from concurrent.futures import ThreadPoolExecutor, Future
from pathlib import Path
from typing import Any, Dict, List, Sequence, Set

from rich.progress import Progress, BarColumn


from .chunks import Builder, Chunk, MarkdownChunk, YAMLDataChunk
from .report import Report
from .utils import write_file, add_notnone


class HTMLBuilder(Builder):
    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        template_file: Path,
        report: Report,
        rebuild_all_pages: bool = True,
        abort_draft: bool = True,
        verbose: bool = False,
        reformat: bool = False,
    ) -> None:
        super().__init__(
            input_path,
            output_path,
            template_file,
            report,
            rebuild_all_pages,
            abort_draft,
            verbose,
            reformat,
        )

    def _transform_page_to_html(
        self,
        chunks: Sequence[Chunk],
        template: str,
        filepath: Path,
        report: Report,
        css: str,
        js: str,
    ) -> str:
        content: Sequence[str] = []
        content.append('<div class="page">')
        if len(chunks) == 0:
            pass
        else:
            first_chunk = chunks[0]
            if isinstance(first_chunk, MarkdownChunk) and not first_chunk.is_section:
                content.append('    <section class="content">')

        for chunk in chunks:
            if (
                "status" in chunk.page_variables
                and self.abort_draft
                and chunk.page_variables["status"] == "draft"
            ):
                content.append("<mark>This site is under construction.</mark>")
                break
            if isinstance(chunk, YAMLDataChunk):
                pass
            elif not chunk.is_ok():
                print("chunk not ok")
                pass
            elif isinstance(chunk, MarkdownChunk):
                if chunk.is_section:
                    # open a new section
                    content.append("    </section>")
                    content.append('    <section class="content">')
                # TODO maybe we want to put the anchor element to the top?
                for aside in chunk.asides:
                    add_notnone(aside.to_html(self), content)
                add_notnone(chunk.to_html(self), content)
            else:
                add_notnone(chunk.to_html(self), content)
                for aside in chunk.asides:
                    add_notnone(aside.to_html(self), content)

        content.append("    </section>")
        content.append("</div>")
        content = "\n".join(content)
        for tag in ["content", "css", "js"]:
            if "{" + tag + "}" not in template:
                self.report.warning(
                    "The template does not contain insertion tag {" + tag + "}"
                )
        return template.format_map({"content": content, "css": css, "js": js})

    def _create_target(
        self,
        source_file_path: Path,
        target_file_path: Path,
        template_file_path: Path,
        overwrite: bool,
    ) -> bool:
        if not target_file_path.is_file():
            return True
        if overwrite:
            return True
        if not template_file_path.is_file():
            return target_file_path.stat().st_mtime < source_file_path.stat().st_mtime
        else:
            return (
                target_file_path.stat().st_mtime < source_file_path.stat().st_mtime
            ) or (target_file_path.stat().st_mtime < template_file_path.stat().st_mtime)

    def _process_file(
        self,
        source_file_path: Path,
        target_file_path: Path,
        template: str,
    ):

        extensions_used: Set[Extension] = set()
        chunks = self.parse_file(source_file_path, extensions_used)
        if not chunks:
            # TODO warn that the page is empty, and therefore nothing is written
            return
        html = self._transform_page_to_html(
            chunks,
            template,
            source_file_path,
            self.report,
            self.core.get_css(self.extensions_used),
            self.core.get_js(self.extensions_used),
        )
        write_file(html, target_file_path, self.report)
        self.report.info("Translated", path=target_file_path)

    def _default_html_template(self) -> str:
        html: Sequence[str] = []
        html.append('<head><title></title><style type="text/css">{css}</style></head>')
        html.append("<body>")
        html.append("{content}")
        html.append("</body>")
        html.append("</html>")
        return "\n".join(html)

    def _load_html_template(self, template_path: Path, report: Report) -> str:
        try:
            with open(
                template_path, "r", encoding="utf-8", errors="surrogateescape"
            ) as templatefile:
                template = templatefile.read()
                self.report.info("Loading template {}.".format(template_path))
                return template
        except FileNotFoundError:
            self.report.warning(
                "Template file missing. Expected at {}. Using default template.".format(
                    template_path
                )
            )
            return self._default_html_template()

    def build(
        self,
    ) -> None:
        template = self._load_html_template(self.template_file, self.report)
        jobs: Sequence[Dict[str, Any]] = []
        files = list(self.input_path.glob("*.md"))
        self.output_path.mkdir(exist_ok=True, parents=True)
        for source_file_path in files:
            target_file_path: Path = self.output_path / (
                source_file_path.stem + ".html"
            )
            if self._create_target(
                source_file_path,
                target_file_path,
                self.template_file,
                self.rebuild_all_pages,
            ):
                jobs.append(
                    {
                        "source_file_path": source_file_path,
                        "target_file_path": target_file_path,
                        "template": template,
                        "abort_draft": self.abort_draft,
                    }
                )
        if len(files) == 0:
            self.report.conclude(
                "No source files (*.md) detected. Searched in {}".format(
                    self.input_path
                )
            )
            return
        elif len(jobs) == 0:
            self.report.conclude(
                "No changed files detected. To re-build all unchanged files, use the [bold]--all[/bold] option."
            )
            return
        if len(jobs) == 1:
            self.report.info("Using single thread.")
            with Progress(transient=True) as progress:
                progress.add_task("[orange]Building 1 page", start=False)
                self._process_file(
                    jobs[0]["source_file_path"],
                    jobs[0]["target_file_path"],
                    jobs[0]["template"],
                )
        else:
            with ThreadPoolExecutor() as e:
                self.report.info("Using threadpool.")
                with Progress(
                    "[progress.description]{task.description}",
                    BarColumn(),
                    "[progress.percentage]{task.percentage:>3.0f}%",
                    transient=True,
                ) as progress:
                    task = progress.add_task(
                        f"[orange]Building {len(jobs)} pages",
                        total=len(jobs),
                    )
                    futures = []
                    for job in jobs:
                        future = e.submit(
                            self._process_file,
                            job["source_file_path"],
                            job["target_file_path"],
                            job["template"],
                        )
                        future.add_done_callback(
                            lambda p: progress.update(task, advance=1.0)
                        )
                        futures.append(future)
                    for future in futures:
                        future.result()


# from watchdog.events import FileSystemEventHandler
# from watchdog.observers import Observer
# def build_html_continuously(
#     self,
#     input_path: Path,
#     output_path: Path,
#     template_path: Path,
#     draft: bool,
#     verbose: bool,
# ):
#     class MyHandler(FileSystemEventHandler):
#         def on_modified(self, event):
#             print(event)
#             self.build()

#     observer = Observer()
#     # event_handler = LoggingEventHandler()
#     # observer.schedule(event_handler, input, recursive=True)
#     observer.schedule(MyHandler(), input, recursive=True)
#     observer.start()
#     try:
#         while True:
#             time.sleep(10)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

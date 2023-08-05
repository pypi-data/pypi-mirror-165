from pathlib import Path
from typing import Any, Dict, Sequence

import requests

from ... import YAMLChunk, YamlExtension, RawChunk, Builder


def download_preview(url: str, target_path: Path):
    if not target_path.exists():
        data = requests.get(url).content
        with open(target_path, "wb") as handler:
            handler.write(data)


class VideoExtension(YamlExtension):
    def __init__(self):
        super().__init__(type=["video", "youtube"], chunk_class=Video)


class Video(YAMLChunk):
    def __init__(
        self,
        raw_chunk: RawChunk,
        dictionary: Dict[str, Any],
        page_variables: Dict[str, Any],
    ):
        super().__init__(
            raw_chunk,
            dictionary,
            page_variables,
            required=["video"],
            optional=["start", "caption", "position"],
        )

    def get_id(self):
        video = self.dictionary["video"]
        return super().create_hash("{}".format(video))

    def to_html(self, builder: Builder):
        html: Sequence[str] = []
        video = self.dictionary["video"]
        url = "https://youtube-nocookie.com/{}".format(video)
        # url = "https://youtu.be/{}".format(video)
        start = ""
        if "start" in self.dictionary:
            start = "?start={}".format(self.dictionary["start"])
            url = url + start
        if "position" in self.dictionary and self.dictionary["position"] == "aside":
            aside_id = self.get_id()
            html.append(
                '<span name="{}"></span><aside name="{}">'.format(aside_id, aside_id)
            )
            html.append(
                '<a href="{}"><img width="{}" src="https://img.youtube.com/vi/{}/sddefault.jpg"></img></a>'.format(
                    url, 240, video
                )
            )
            if "caption" in self.dictionary:
                html.append(
                    builder.convert(
                        self.dictionary["caption"],
                        target_format="html",
                        source_format="md",
                    )
                )
            html.append("</aside>")
        else:
            html.append('<div class="figure">')
            width = 560
            height = 315
            # TODO set the title element of an iframe to improve accessibility scores
            html.append(
                '<iframe width="{}" height="{}" src="https://www.youtube-nocookie.com/embed/{}{}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'.format(
                    width, height, video, start
                )
            )
            if "caption" in self.dictionary:
                html.append(
                    '<span name="{}">&nbsp;</span>'.format(self.dictionary["video"])
                )
                html.append(
                    '<aside name="{}"><p>{}</p></aside>'.format(
                        self.dictionary["video"],
                        builder.convert(
                            self.dictionary["caption"],
                            target_format="html",
                            source_format="md",
                        ),
                    )
                )
            html.append("</div>")
        return "\n".join(html)

    def to_latex(self, builder: Builder) -> str:
        s: Sequence[str] = []
        url = "https://img.youtube.com/vi/{}/sddefault.jpg".format(
            self.dictionary["video"]
        )
        video_url = "https://youtu.be/{}".format(self.dictionary["video"])
        video_id = self.get_id()
        target_path = self.get_dir_cached() / "{}.jpg".format(video_id)
        download_preview(url, target_path)
        # target_path =  Path('../cached/{}.jpg'.format(video_id))
        target_path = target_path.relative_to(builder.output_file.parent)
        s.append(r"\n")
        s.append(r"\\begin{video}[h]")
        s.append(r"\includegraphics[width=\linewidth]{{{}}}".format(target_path))
        if "caption" in self.dictionary:
            s.append(
                r"\caption{"
                + builder.convert(
                    self.dictionary["caption"],
                    target_format="latex",
                    source_format="md",
                )
                + r" \textcolor{SteelBlue}{\faArrowCircleRight}~"
                + r"\\url{{{}}}".format(video_url)
                + r"}"
            )
        else:
            s.append(r"\caption{")
            s.append(r"\\url{{{}}}".format(video_url) + "}")
        s.append(r"\end{video}")
        return r"\n".join(s)

from pathlib import Path
from typing import Any, Dict, Sequence
import random

import requests

from ... import YAMLChunk, YamlExtension, RawChunk, Builder


class QuizExtension(YamlExtension):
    def __init__(self):
        super().__init__(type="quiz", chunk_class=Quiz)


class Alternative:
    def __init__(self, correct: bool, text: str, result: str) -> None:
        self.correct = correct
        self.text = text
        self.result = result


class Quiz(YAMLChunk):
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
            required=["correct", "false-1"],
            optional=[
                "question",
                "title", "false-2", "false-3",
                "result-correct",
                "result-false",
                "result-false-1",
                "result-false-2",
                "result-false-3",
            ],
        )
        # we check how many alternatives there are
        if "false-3" in dictionary:
            if "false-2" not in dictionary:
                self.raw_chunk.report.error("Attribute false-2 is missing.")
                self.is_ok = False
            self.n_alternatives = 4
        elif "false-2" in dictionary:
            self.n_alternatives = 3
        else:
            self.n_alternatives = 2

        self.quiz_id = self.raw_chunk.get_hash()
        random.seed(self.quiz_id)
        self.correct_alternative = random.choice(list(range(self.n_alternatives)))

        if "title" in dictionary:
            self.title = dictionary["title"]
        else:
            self.title = "Question"

        if "question" in dictionary:
            self.question: str = dictionary["question"]
        elif self.has_post_yaml():
            self.question = self.get_post_yaml()
        else:
            self.question = "Question is missing."
            self.error(
                "Question must either be given as question attribute or post-yaml section."
            )

        self.alternatives: Sequence[Alternative] = []
        for i in list(range(1,self.n_alternatives)):
            self.alternatives.append(
                Alternative(
                    False,
                    dictionary[f"false-{i}"],
                    dictionary[f"result-false-{i}"]
                    if f"result-false-{i}" in dictionary
                    else dictionary["result-false"]
                    if "result-false" in dictionary
                    else "<b>Wrong.</b>",
                )
            )
        self.alternatives.insert(
            self.correct_alternative,
            Alternative(
                True,
                dictionary["correct"],
                dictionary["result-correct"]
                if "result-correct" in dictionary
                else "<b>Correct!</b>",
            ),
        )

    def get_id(self):
        video = self.dictionary["video"]
        return super().create_hash("{}".format(video))

    def to_html(self, builder: Builder):
        html: Sequence[str] = []
        html.append(f'<div class="card mb-5 shadow-sm" id="{self.quiz_id}">')
        html.append('  <div class="card-body">')
        html.append(f'    <h5 class="card-title">{self.title}</h5>')
        html.append(
            f'    <div class="card-text">{builder.convert(self.question, target_format="html")}</div>'
        )
        html.append("</div>")
        html.append('<ol class="list-group list-group-flush quiz">')
        for i, alternative in enumerate(self.alternatives):
            html.append(
                f'<li class="list-group-item unselected" onclick="quiz_select(\'{self.quiz_id}\', {i})">{alternative.text}</li>'
            )
        html.append("</ol>")
        html.append('<div class="card-footer">')
        html.append('<div data="instructions">')
        html.append("  <i>Select the alternative that matches best.</i>")
        html.append("</div>")
        html.append('<div class="visually-hidden" data="confirm">')
        html.append(
            f'  <i>Sure? Then <a class="disabled" onclick="quiz_confirm(\'{self.quiz_id}\', {self.correct_alternative})">confirm</a>.</i>'
        )
        html.append("</div>")
        for i, alternative in enumerate(self.alternatives):
            html.append(
                f'<div class="visually-hidden" data="{i}">{alternative.result}</div>'
            )
        html.append("</div>")
        html.append("</div>")
        return "\n".join(html)

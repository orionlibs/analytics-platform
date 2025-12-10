import argparse
import shutil
import tempfile
import yaml
import graphviz
import hashlib
from dataclasses import dataclass, field


@dataclass
class RawStep:
    name: str
    depends_on: list[str]


@dataclass
class RawPipeline:
    name: str
    depends_on: list[str]
    steps: list[RawStep]


def calc_id(name: str, prefix_id: str = "") -> str:
    def normalise(s: str) -> str:
        hash = hashlib.sha256(s.encode(), usedforsecurity=False).hexdigest()
        s = s.lower()
        s = s.replace("-", "_")
        s = s.replace(" ", "_")
        s = s.replace(".", "_")
        s = s.replace(":", "_")
        s = s + "_" + hash[:12]
        return s

    name = normalise(name)

    if prefix_id:
        name = prefix_id + "__" + name
    return name


@dataclass(unsafe_hash=True)
class Step:
    label: str = field(hash=False)
    id: str = field(hash=True)
    depends_on: set[str] = field(hash=False, default_factory=lambda: set())
    dependents: set[str] = field(hash=False, default_factory=lambda: set())


@dataclass(unsafe_hash=True)
class Pipeline:
    label: str = field(hash=False)
    id: str = field(hash=True)
    steps: list[Step] = field(hash=False, default_factory=lambda: [])
    depends_on: set[str] = field(hash=False, default_factory=lambda: set())
    dependents: set[str] = field(hash=False, default_factory=lambda: set())


def read_raw_pipelines(file: str) -> list[RawPipeline]:
    "Read the raw .drone.yml file. This adds no additional metadata, and does not additional processing."
    with open(file, "r") as f:
        drone = yaml.safe_load_all(f)
        drone = list(drone)

    drone = [x for x in drone if x["kind"] == "pipeline"]

    pipelines: list[RawPipeline] = []
    for pipeline in drone:
        if "steps" not in pipeline:
            continue

        steps: list[RawStep] = []
        for step in pipeline["steps"]:
            steps.append(RawStep(step["name"], step.get("depends_on", [])))
        pipelines.append(
            RawPipeline(pipeline["name"], pipeline.get("depends_on", []), steps)
        )

    return pipelines


def read_pipeline(file: str) -> list[Pipeline]:
    """Read the raw .drone.yml file and transform into something more useful.

    Don't analyse the complexity of this. It will make you cry.
    """
    raw = read_raw_pipelines(file)

    pipelines: list[Pipeline] = []
    for raw in raw:
        pipe = Pipeline(raw.name, calc_id(raw.name))
        pipe.depends_on = set([calc_id(x) for x in raw.depends_on])

        for step in raw.steps:
            step_id = calc_id(step.name, pipe.id)
            depends_on = set([calc_id(x, pipe.id) for x in step.depends_on])
            pipe.steps.append(Step(step.name, step_id, depends_on=depends_on))

        pipelines.append(pipe)

    for p1 in pipelines:
        for d in p1.depends_on:
            for p2 in pipelines:
                if d == p2.id:
                    p2.dependents.add(p1.id)
                    break
        for s1 in p1.steps:
            for d in s1.depends_on:
                for s2 in p1.steps:
                    if d == s2.id:
                        s2.dependents.add(s1.id)
                        break

    return pipelines


def generate_graph(pipelines: list[Pipeline], file: str, format: str) -> graphviz.Digraph:
    dot = graphviz.Digraph(name=file, comment="The Drone pipelines.")
    dot.format = format

    # Declare all pipelines first.
    for pipeline in pipelines:
        dot.node(pipeline.id, pipeline.label)
    # Then their dependencies.
    for pipeline in pipelines:
        for dep in pipeline.depends_on:
            dot.edge(pipeline.id, dep)

    for pipeline in pipelines:
        if len(pipeline.steps) == 0:
            continue

        # Now, we can add the steps as subgraphs...
        with dot.subgraph(name=f"cluster_{pipeline.id}") as g:
            g.attr(style="filled", color="lightgrey")
            g.node_attr.update(style="filled", color="white", shape="box")

            for step in pipeline.steps:
                g.node(step.id, step.label)

            for step in pipeline.steps:
                for dep in step.depends_on:
                    g.edge(step.id, dep)

        for step in pipeline.steps:
            if len(step.dependents) == 0:
                dot.edge(pipeline.id, step.id)

    return dot


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="drone-graph", description="Generate graphs from Drone pipelines."
    )
    _ = parser.add_argument(
        "-f", "--file", help="the Drone pipeline YAML file", default=".drone.yml"
    )
    _ = parser.add_argument(
        "-o",
        "--output",
        help="the path to output the graph to",
        default=".drone.yml.svg",
    )
    _ = parser.add_argument("-t", "--type", help="the output format type ('svg', 'png', 'pdf')", default='svg')
    args = parser.parse_args()
    inputFile: str = args.file
    outputFile: str = args.output
    outputFormat: str = args.type

    pipelines = read_pipeline(inputFile)
    graph = generate_graph(pipelines, inputFile, outputFormat).unflatten(stagger=3)

    with tempfile.NamedTemporaryFile(suffix=".gv") as gv:
        written = graph.render(gv.name)
        shutil.move(written, outputFile)

    return 0

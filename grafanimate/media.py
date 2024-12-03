import os.path

from grafanimate.model import AnimationScenario, RenderingOptions
from grafanimate.postprocessing import MediaProducer
from grafanimate.util import ensure_directory, slug


def produce_artifacts(
    input,
    output,
    scenario: AnimationScenario,
    options: RenderingOptions,
):
    # TODO: Can use dashboard title as output filename here?
    # TODO: Can put `start` into filename?

    title_slug = slug(scenario.dashboard_title or scenario.dashboard_uid)
    if scenario.source is not None:
        scenario_slug = slug(scenario.source.replace(".py", ""))
    else:
        scenario_slug = None

    # Compute input pattern and output file name.
    input = os.path.join(str(input), "*.png")
    output = str(output).format(
        scenario=scenario_slug,
        title=title_slug,
        uid=scenario.dashboard_uid,
    )

    # Produce output artifacts.
    ensure_directory(output)
    producer = MediaProducer(options=options)
    return producer.render(source=input, target=output)

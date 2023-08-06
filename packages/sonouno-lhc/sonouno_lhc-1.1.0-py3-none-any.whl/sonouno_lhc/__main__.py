from importlib import resources
from pathlib import Path

from sonouno_lhc import data
from sonouno_lhc.lhc_data import sonify_event
from sonouno_lhc.io import extract_events

DATA = resources.files(data)
OUTPUT_PATH = Path('sonouno-lhc-outputs')
OUTPUT_PATH.mkdir(exist_ok=True)


def sonify_events(path: Path, include_plot) -> None:
    data = path.read_text().split('\n')
    for event in extract_events(data):
        sound, fig = sonify_event(event, include_plot=include_plot)

        if include_plot:
            assert fig is not None
            # Save the plot
            plot_path = OUTPUT_PATH / f'plot-dataset-{event.id}.png'
            fig.savefig(plot_path, format='png')

        # Generate the wav file with the sonification
        sound_path = OUTPUT_PATH / f'sound-dataset-{event.id}.wav'
        sound.to_wav(sound_path)


sonify_events(DATA / 'sonification_reduced.txt', False)

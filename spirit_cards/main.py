from spirit_cards.constants import FRAME_RATE
from spirit_cards.main_scenes.load_scene.load_scene import LoadScene, LoadSceneParameters
from spirit_cards.pygame_extension.pygame_engine import PygameConfiguration, PygameEngine
from spirit_cards.example_code.example_scene import ExampleScene
from spirit_cards.services.asset_manager import AssetManager
from spirit_cards.services.global_services import ASSET_MANAGER

def main():

    engine = PygameEngine({
        ASSET_MANAGER: AssetManager()
    })

    configuration = PygameConfiguration(
        start_scene = LoadScene,
        start_scene_parameters = LoadSceneParameters(
            scene = ExampleScene,
            load_files = {
                "test": "image"
            }
        ),
        frame_rate = FRAME_RATE
    )

    print(f"Starting PygameEngine with the following parameters:\n{vars(configuration)}")

    try:
        engine.run(configuration)
    except:
        print("Game ungracefully stopped because of an exception")
        raise
    
    engine.cleanup

if __name__ == "__main__":
    main()
from spirit_cards.asset_map import MONTSERRAT_24, TEST_CARD, TEST_SPRITE_SHEET, TEST_TILE
from spirit_cards.constants import FRAME_RATE
from spirit_cards.example_code.board_prototype_scene import BoardPrototypeScene
from spirit_cards.example_code.secondary_scene import SecondaryScene
from spirit_cards.pygame_extension.load_scene.asset_loader import FontLoadParams, AssetLoadConfiguration
from spirit_cards.pygame_extension.load_scene.load_scene import LoadScene, LoadSceneParameters
from spirit_cards.pygame_extension.pygame_engine import PygameConfiguration, PygameEngine
from spirit_cards.example_code.example_scene import ExampleScene
from spirit_cards.services.asset_manager import AssetManager, AssetType
from spirit_cards.services.global_services import GlobalServices

def main():

    engine = PygameEngine({
        GlobalServices.ASSET_MANAGER: AssetManager()
    })

    configuration = PygameConfiguration(
        start_scene = LoadScene,
        start_scene_parameters = LoadSceneParameters(
            scene = BoardPrototypeScene,
            load_files = {
                TEST_SPRITE_SHEET: AssetLoadConfiguration(type=AssetType.Image),
                TEST_TILE: AssetLoadConfiguration(type=AssetType.Image),
                TEST_CARD: AssetLoadConfiguration(type=AssetType.Image),

                MONTSERRAT_24: AssetLoadConfiguration(type=AssetType.Font, parse_parameters={FontLoadParams.FONT_SIZE: 24})
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
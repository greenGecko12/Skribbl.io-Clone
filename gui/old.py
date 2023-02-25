'''
Contains bits of code from the app.py file that aren't needed anymore
'''

# we don't need any examples
# with gr.Row():
#     example_weights = gr.Dataset(
#         components=[structure_weight, color_weight],
#         samples=[
#             [0.6, 1.0],
#             [0.3, 1.0],
#             [0.0, 1.0],
#             [1.0, 0.0],
#         ])


# We don't need any examples
# with gr.Row():
#     example_styles = gr.Dataset(
#         components=[style_type, style_index],
#         samples=[
#             ['cartoon', 26],
#             ['caricature', 65],
#             ['arcane', 63],
#             ['pixar', 80],
#         ])


# providing examples images (not necessary for us)
# with gr.Row(): 
#     paths = sorted(pathlib.Path('images').glob('*.jpg'))
#     example_images = gr.Dataset(components=[input_image],
#                                 samples=[[path.as_posix()]
#                                          for path in paths])


# def get_style_image_url(style_name: str) -> str:
#     base_url = 'https://raw.githubusercontent.com/williamyang1991/DualStyleGAN/main/doc_images'
#     filenames = {
#         'cartoon': 'cartoon_overview.jpg',
#     }
#     return f'{base_url}/{filenames[style_name]}'

#  style_type = gr.Radio(
#                                         #   model.style_types,
#                                         [ "cartoon" ],
#                                           label='Style Type')

# style_type.change(fn=update_slider,
#                     inputs=style_type,
#                     outputs=style_index)


# style_type.change(fn=update_style_image,
#                     inputs=style_type,
#                     outputs=style_image)

# def update_slider(choice: str) -> dict:
#     max_vals = {
#         'cartoon': 316,
#     }
#     return gr.Slider.update(maximum=max_vals[choice])


# def update_style_image(style_name: str) -> dict:
#     text = get_style_image_markdown_text(style_name)
#     return gr.Markdown.update(value=text)

# example_images.click(fn=set_example_image,
#                      inputs=example_images,
#                      outputs=example_images.components)
# example_styles.click(fn=set_example_styles,
#                      inputs=example_styles,
#                      outputs=example_styles.components)
# example_weights.click(fn=set_example_weights,
#                       inputs=example_weights,
#                       outputs=example_weights.components)

# def set_example_image(example: list) -> dict:
#     return gr.Image.update(value=example[0])


# def set_example_styles(example: list) -> list[dict]:
#     return [
#         gr.Radio.update(value=example[0]),
#         gr.Slider.update(value=example[1]),
#     ]


# def set_example_weights(example: list) -> list[dict]:
#     return [
#         gr.Slider.update(value=example[0]),
#         gr.Slider.update(value=example[1]),
#     ]

# def parse_args() -> argparse.Namespace:
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--device', type=str, default='cpu')
#     parser.add_argument('--theme', type=str)
#     parser.add_argument('--share', action='store_true')
#     parser.add_argument('--port', type=int)
#     parser.add_argument('--disable-queue', dest='enable_queue', action='store_false')
#     return parser.parse_args()
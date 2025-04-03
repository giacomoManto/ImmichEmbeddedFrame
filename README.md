# Immich Embedded Frame

Interfaces with Immich api to pull, process, and display images for embedded devices.

1. Various displays can be implemented by extending [BaseDisplayManager](display/base_display_manager.py) and adding the new display manager in [get_display_manager](display/get_display_manager.py).
2. Similar situation with extending [photo processing](photo_processing/ImageProcessor.py) capabilities
3. Same for adding classes to [image_fetcher/search_handlers](image_fetcher/search_handlers/) to specify different types of image queries.

Take a look at [example_config.yaml](config/example_config.yaml) and [get_config](config/config_handler) to setup connection to your server.

## To Do

1. Complete [daemon/main.py](daemon/main.py) to be runnable as both a daemon and a script.
2. Add threading to [daemon/main.py](daemon/main.py) to more effectively handle both display and image fetching/processing.
3. Add socket listening to send commands while running in background.
4. Improve customizability of photo order/display
5. Make log output to file (if specified) when not running in background.
6. Handle changing image_processing modes (e.g. rotate=True, "maintain"...) on the fly.
7. (Maybe) Add Clock

## Current Hardware

This setup has been tested exclusively with a rasberry pi zero 2w displaying to a [Waveshare epd7in3e](https://www.waveshare.com/product/displays/e-paper/epaper-1/7.3inch-e-paper-hat-e.htm).

## Setup

1. `git clone git@github.com:giacomoManto/Immich-Frame.git`
2. `pip install uv`
3. `cd Immich-Frame`
4. `cp example_config.yaml config.yaml`
5. Edit you config to point at your api endpoints with correct api key.
6. `uv run main.py`

## Run Example With Immich Demo

1. `git clone git@github.com:giacomoManto/Immich-Frame.git`
2. `pip install uv`
3. `cd ImmichEmbeddedFrame`
4. `cp config/example_config.yaml config/config.yaml`
5. Go to [https://demo.immich.app/](https://demo.immich.app/) use demo login and in account settings get an api key.
6. Fill out [config/config.yaml](config/config.yaml)
7. `uv run main.py`

## Run Simulated Example

1. `git clone git@github.com:giacomoManto/Immich-Frame.git`
2. `pip install uv`
3. `cd Immich-Frame`
4. `uv run example.py`

### Example Photo Credits

[sergio-kian-unsplash.jpg](example/original/sergio-kian-unsplash.jpg)<br>
by <a href="https://unsplash.com/@sergiokian?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Sergio Kian</a> on <a href="https://unsplash.com/photos/mountains-rise-above-a-hazy-forested-landscape-bCPxqVjC5uc?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a><br>
[karsten-winegeart-unsplash.jpg](example/original/karsten-winegeart-unsplash.jpg)<br>by <a href="https://unsplash.com/@karsten116?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Karsten Winegeart</a> on <a href="https://unsplash.com/photos/dramatic-mountains-under-a-cloudy-moody-sky-9DyNN_Yz2yk?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a><br>
[simon-berger-unsplash.jpg](example/original/simon-berger-unsplash.jpg)<br>by <a href="https://unsplash.com/@simon_berger?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Simon Berger</a> on <a href="https://unsplash.com/photos/a-branch-of-a-tree-with-pink-flowers-lCjH6ZOBhXs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash">Unsplash</a>

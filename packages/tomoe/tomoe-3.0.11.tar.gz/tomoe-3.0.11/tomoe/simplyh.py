import janda
import requests
import os
import re
import time
from .utils.misc import (
    choose,
    split_name,
    get_size,
    convert_html_to_pdf,
    project,
    get_size_folder,
    nums,
    log_data,
    log_file,
    log_final,
)
from inputimeout import inputimeout, TimeoutOccurred

simply = janda.SimplyHentai()
t: str = "tomoe.html"


async def get_sim(id: str = choose().simply):
    initial = time.time()
    data = await simply.get(id)
    parser = janda.resolve(data)

    title = re.sub(r"[^\w\s]", "", parser["data"]["title"])
    img = parser["data"]["image"]
    number = parser["data"]["id"]
    tags = parser["data"]["tags"]
    tags = [tag for tag in tags]
    to_tags = ", ".join(tags)

    log_data("TITLE", title)
    log_data("TAGS", to_tags)
    log_data("ID", number)
    log_data("SOURCE", parser["source"])
    log_data("TOTAL", f"{parser['data']['total']} pages")

    neat_dir = f"{split_name(__file__)}-{title}"
    neat_dir = re.sub("[^A-Za-z0-9-]+", " ", neat_dir)

    neat_dir = re.sub(r"\s+", "_", neat_dir)

    set_name = parser["data"]["id"]
    set_name = set_name.split("/")[-1]

    if not os.path.exists(neat_dir):
        os.makedirs(neat_dir)

    if len(os.listdir(neat_dir)) - 1 == len(img):
        print(
            "All images already downloaded! If you're doubt kindly remove this folder and re-download"
        )
        print(f"Directory: {os.path.abspath(neat_dir)}")
        return

    for i in range(len(img)):
        start = time.time()
        r = requests.get(img[i])
        with open(f"{neat_dir}/{i+1}.jpg", "wb") as f:
            f.write(r.content)

            if os.path.exists(f"{neat_dir}/{i+1}.jpg"):
                file = get_size(f"{neat_dir}/{i+1}.jpg")
                log_file(i + 1, file, f"{time.time() - start:.2f}")
                ## print(f"Successfully downloaded {i+1} | {file} MB | took {time.time() - start:.2f} seconds")

            if len(img) == len(os.listdir(neat_dir)):
                log_final(
                    f"{(time.time() - initial) / 60:.2f}", get_size_folder(neat_dir)
                )

                print(f"Directory: {os.path.abspath(neat_dir)}")

                with open(neat_dir + "/" + t, "x", encoding="utf-8") as f:
                    f.write("<html><center><body>")
                    f.write(f"<h1>{neat_dir}</h1>")

                    for i in nums(1, len(img)):

                        f.write(f'<img src="{neat_dir}/{i}.jpg"><p></p>')
                    f.write(f"{project()}")
                    f.write("</body></center></html>")
                    f.close()

                try:
                    desired = inputimeout(
                        prompt="Do you want to render it all to .pdf? (y/n) ",
                        timeout=7,
                    )
                    to_pdf = desired

                    if to_pdf == "y":
                        try:
                            source = open(f"{neat_dir}/{t}")
                            output = f"{neat_dir}/{set_name}.pdf"
                            filepdf = output.rsplit("/", 1)[-1]

                            convert_html_to_pdf(source, output)
                            print(
                                f"Successfully rendered to {filepdf} | {get_size(output)} MB"
                            )

                        except Exception as e:
                            print(f"Something went wrong while converting to pdf: {e}")

                    elif to_pdf == "n":
                        print("Okay")
                        os.remove(neat_dir + "/" + t)
                        return

                    else:
                        print("Invalid input")
                        os.remove(neat_dir + "/" + t)
                        return

                except TimeoutOccurred:
                    print("Timeout occurred")
                    os.remove(neat_dir + "/" + t)
                    exit()

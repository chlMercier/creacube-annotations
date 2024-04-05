# CreaCube annotations

## Goal

This project extends the [CreaMaker](https://creamaker.wordpress.com/) project to study creative problem-solving activities. We focus here on the CreaCube task, which consists of building a vehicle from modular robotic cubelets. A few hundreds of participants have already been filmed while performing the task.

At the moment, videos of the participants are manually annotated using an encoding detailed in `annotation-codes.pdf`. We wish to automatize this annotation process using computer vision. [Théo Carme](https://github.com/TheoCarme) has developed a first model available [here](https://github.com/TheoCarme/CreaCube) as part of his Masters' internship. The logs returned by this model include the coordinates of the cubes' bounding boxes, and we would like to convert such logs into sequences of observations encoded as proposed in `annotation-codes.pdf`.

## Content of this repository

`configurations.json` contains the list of annotation codes as a JSON file, where each configuration is detailed as a set of connections between the cubes, oriented along x,y or z axes (in a direct basis).

`display3d.py` is a little script alowing to display a 3d model of a configuration given its annotation code. A notebook Jupyter version is also available (`display3d.ipynb`).

The `in-out_examples` folder contain examples of logs returned by the computer vision model (in) and logs manually annotated (out). This project aims to transform the former into the latter.

## How to install and run

Install the requirements, preferably in a virtual environment; we recommend using Pipenv:

```pipenv install```

then activate the environment using

```pipenv shell```

As soon as your environment is activated, you can run the following command `python3 display3d.py -cc [code]` to display a configuration. Note that vpython works better with the Chrome browser. For example, if you want to display the configuration "F030-SWBI":

```
python3 display3d.py -cc "F030-SWBI"
```

You may prefer to run it through the notebook. Create a Jupyter kernel within the Pipenv environment:

```python -m ipykernel install --user --name=creacube-annotations```

Now you can launch jupyter notebook:

```jupyter notebook```

In your notebook, Kernel -> Change Kernel and set it to creacube-annotations.
You're good to go!
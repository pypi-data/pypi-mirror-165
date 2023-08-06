ferret
========

|pypi badge| |docs badge| |demo badge| |youtube badge| |arxiv badge| |downloads badge|

|banner|

.. |pypi badge| image:: https://img.shields.io/pypi/v/ferret-xai.svg
    :target: https://pypi.python.org/pypi/ferret-xai
    :alt: Latest PyPI version

.. |Docs Badge| image:: https://readthedocs.org/projects/ferret/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://ferret.readthedocs.io/en/latest/?version=latest

.. |demo badge| image:: https://img.shields.io/badge/HF%20Spaces-Demo-yellow
    :alt: HuggingFace Spaces Demo 
    :scale: 100%
    :target: https://huggingface.co/spaces/g8a9/ferret

.. |youtube badge| image:: https://img.shields.io/badge/youtube-video-red
    :alt: YouTube Video
    :scale: 100%
    :target: https://www.youtube.com/watch?v=kX0HcSah_M4

.. |banner| image:: /_static/banner.png
    :alt: Ferret circular logo with the name to the right
    :scale: 100%
    
.. |arxiv badge| image:: https://img.shields.io/badge/arXiv-2208.01575-b31b1b.svg
    :alt: arxiv preprint
    :scale: 100%
    :target: https://arxiv.org/abs/2208.01575
    
.. |downloads badge| image:: https://pepy.tech/badge/ferret-xai
    :alt: downloads badge
    :scale: 100%
    :target: https://pepy.tech/project/ferret-xai


A python package for benchmarking interpretability techniques.

* Free software: MIT license
* Documentation: https://ferret.readthedocs.io.

.. code-block:: python

    from transformers import AutoModelForSequenceClassification, AutoTokenizer
    from ferret import Benchmark

    name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(name)
    tokenizer = AutoTokenizer.from_pretrained(name)

    bench = Benchmark(model, tokenizer)
    explanations = bench.explain("You look stunning!", target=1)
    evaluations = bench.evaluate_explanations(explanations, target=1)

    bench.show_evaluation_table(evaluations)

Features
--------

**ferret** offers a *painless* integration with Hugging Face models and naming conventions. If you are already using the `transformers <https://github.com/huggingface/transformers>`_ library, you immediately get access to our **Explanation and Evaluation API**.

Supported Post-hoc Explainers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Gradient (plain gradients or multiplied by input token embeddings) (`Simonyan et al., 2014 <https://arxiv.org/abs/1312.6034>`_)
* Integrated Gradient (plain gradients or multiplied by input token embeddings) (`Sundararajan et al., 2017 <http://proceedings.mlr.press/v70/sundararajan17a.html>`_)
* SHAP (via Partition SHAP approximation of Shapley values) (`Lundberg and Lee, 2017 <https://proceedings.neurips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html>`_)
* LIME (`Ribeiro et al., 2016 <https://dl.acm.org/doi/abs/10.1145/2939672.2939778>`_)

Supported Evaluation Metrics
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Faithfulness** measures:

* AOPC Comprehensiveness (`DeYoung et al., 2020 <https://doi.org/10.18653/v1/2020.acl-main.408>`_)
* AOPC Sufficiency (`DeYoung et al., 2020 <https://doi.org/10.18653/v1/2020.acl-main.408>`_)
* Kendall’s Tau correlation with Leave-One-Out token removal. (`Jain and Wallace, 2019 <https://aclanthology.org/N19-1357/>`_)

**Plausibility** measures:

* Area-Under-Precision-Recall-Curve (soft score) (`DeYoung et al., 2020 <https://doi.org/10.18653/v1/2020.acl-main.408>`_)
* Token F1 (hard score) (`DeYoung et al., 2020 <https://doi.org/10.18653/v1/2020.acl-main.408>`_)
* Token Intersection Over Union (hard score) (`DeYoung et al., 2020 <https://doi.org/10.18653/v1/2020.acl-main.408>`_)

See our `paper <https://arxiv.org/abs/2208.01575>`_  for details.

Visualization
-------------

The `Benchmark` class exposes easy-to-use table visualization methods (e.g., within Jupyter Notebooks)  

.. code-block:: python

    bench = Benchmark(model, tokenizer)

    # Pretty-print feature attribution scores by all supported explainers
    explanations = bench.explain("You look stunning!")
    bench.show_table(explanations)

    # Pretty-print all the supported evaluation metrics
    evaluations = bench.evaluate_explanations(explanations)
    bench.show_evaluation_table(evaluations)


Dataset Evaluations
-------------------

The `Benchmark` class has a handy method to compute and average our evaluation metrics across multiple samples from a dataset.

.. code-block:: python

    import numpy as np
    bench = Benchmark(model, tokenizer)

    # Compute and average evaluation scores one of the supported dataset
    samples = np.arange(20)
    hatexdata = bench.load_dataset("hatexplain")
    sample_evaluations =  bench.evaluate_samples(hatexdata, samples)
    
    # Pretty-print the results
    bench.show_samples_evaluation_table(sample_evaluations)

Credits
-------

This package was created with Cookiecutter and the *audreyr/cookiecutter-pypackage* project template.

- Cookiecutter: https://github.com/audreyr/cookiecutter
- `audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

Logo and graphical assets made by `Luca Attanasio <https://www.behance.net/attanasiol624d>`_.

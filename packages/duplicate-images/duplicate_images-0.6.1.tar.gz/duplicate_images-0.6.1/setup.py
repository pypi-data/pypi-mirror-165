# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['duplicate_images']

package_data = \
{'': ['*']}

install_requires = \
['Wand>=0.6.5,<0.7.0',
 'coloredlogs>=15.0,<16.0',
 'imagehash>=4.2.1,<5.0.0',
 'pillow-heif>=0.6.1,<0.7.0',
 'pillow>=9.0.1,<10.0.0',
 'tqdm>=4.56.0,<5.0.0']

entry_points = \
{'console_scripts': ['find-dups = duplicate_images.duplicate:main']}

setup_kwargs = {
    'name': 'duplicate-images',
    'version': '0.6.1',
    'description': 'Finds equal or similar images in a directory containing (many) image files',
    'long_description': '# Finding Duplicate Images\n\nFinds equal or similar images in a directory containing (many) image files.\n\nOfficial home page: https://github.com/lene/DuplicateImages\n\nDevelopment page: https://gitlab.com/lilacashes/DuplicateImages\n\nPyPI page: https://pypi.org/project/duplicate-images/0.6.0\n\n## Usage\n\nInstalling:\n```shell\n$ pip install duplicate_images\n```\n\nPrinting the help screen:\n```shell\n$ find-dups -h\n```\n\nQuick test run:\n```shell\n$ find-dups $IMAGE_ROOT \n```\n\nTypical usage:\n```shell\n$ find-dups $IMAGE_ROOT --parallel --progress --hash-db hashes.pickle\n```\n\n### Supported image formats\n\n* JPEG and PNG (tested quite thoroughly)\n* HEIC (experimental support, tested cursorily only)\n\n### Image comparison algorithms\n\nUse the `--algorithm` option to select how equal images are found. The default algorithm is `phash`.\n\n`ahash`, `colorhash`, `dhash`, `phash`, `whash`: five different image hashing algorithms. See \nhttps://pypi.org/project/ImageHash for an introduction on image hashing and \nhttps://tech.okcupid.com/evaluating-perceptual-image-hashes-okcupid for some gory details which\nimage hashing algorithm performs best in which situation. For a start I recommend using `phash`, \nand only evaluating the other algorithms if `phash` does not perform satisfactorily in your use \ncase.\n\n### Image similarity threshold configuration\n\nUse the `--max-distance` parameter to tune how close images should be to be considered duplicates.\nThe argument is a positive integer. Its value is highly dependent on the algorithm used and the \nnature of the images compared, so the best value for your use case can oly be found through \nexperimentation.\n\n### Actions for matching image pairs\n\nUse the `--on-equal` option to select what to do to pairs of equal images. The default action is \n`print`.\n- `delete-first` or `d1`: deletes the first of the two files\n- `delete-second` or `d2`: deletes the second of the two files\n- `delete-bigger` or `d>`: deletes the file with the bigger size\n- `delete-smaller` or `d<`: deletes the file with the smaller size\n- `eog`: launches the `eog` image viewer to compare the two files\n- `xv`: launches the `xv` image viewer to compare the two files\n- `print`: prints the two files\n- `quote`: prints the two files with quotes around each \n- `none`: does nothing.\n  \n### Parallel execution\n\nUse the `--parallel` option to utilize all free cores on your system. \n\n### Progress and verbosity control\n\n- `--progress` prints a progress bar each for the process of reading the images, and the process of \n  finding duplicates among the scanned image\n- `--debug` prints debugging output\n- `--quiet` decreases the log level by 1 for each time it is called; `--debug` and `--quiet` cancel\n  each other out\n\n### Pre-storing and using image hashes to speed up computation\n\nUse the `--hash-db $PICKLE_FILE` option to store image hashes in the file `$PICKLE_FILE` and read\nimage hashes from that file if they are already present there. This avoids having to compute the \nimage hashes anew at every run and can significantly speed up run times.\n\n## Development notes\n\nNeeds Python3, Pillow imaging library and `pillow-heif` HEIF plugin to run, additionally Wand for \nthe test suite.\n\nUses Poetry for dependency management.\n\n### Installation\n\nFrom source:\n```shell\n$ git clone https://gitlab.com/lilacashes/DuplicateImages.git\n$ cd DuplicateImages\n$ pip3 install poetry\n$ poetry install\n```\n\n### Running\n\n```shell\n$ poetry run find-dups $PICTURE_DIR\n```\nor\n```shell\n$ poetry run find-dups -h\n```\nfor a list of all possible options.\n\n### Test suite\n\nRunning it all:\n```shell\n$ poetry run pytest\n$ poetry run mypy duplicate_images tests\n$ poetry run flake8\n$ poetry run pylint duplicate_images tests\n```\nor simply \n```shell\n$ .git_hooks/pre-push\n```\nSetting the test suite to be run before every push:\n```shell\n$ cd .git/hooks\n$ ln -s ../../.git_hooks/pre-push .\n```\n\n### Publishing\n\nThere is a job in GitLab CI for publishing to `pypi.org` that runs as soon as a new tag is added. \nThe tag needs to be the same as the `version` in the `pyproject.toml` file or else the job will \nfail.\n\nTo publish the package on PyPI manually:\n```shell\n$ poetry config repositories.testpypi https://test.pypi.org/legacy/\n$ poetry build\n$ poetry publish --username $PYPI_USER --password $PYPI_PASSWORD --repository testpypi && \\\n  poetry publish --username $PYPI_USER --password $PYPI_PASSWORD\n```\n(obviously assuming that username and password are the same on PyPI and TestPyPI)\n\n#### Updating GitHub mirror\n\nGitHub is set up as a push mirror in GitLab CI, but mirroring is flaky at the time and may not\nsucceed. \n\nTo push to the GitHub repository manually (assuming the GitHub repository is set up as remote \n`github`):\n```shell\n$ git checkout master\n$ git fetch\n$ git pull --rebase\n$ git tag  # to check that the latest tag is present\n$ git push --tags github master \n```\n\n### Profiling\n\n#### CPU time\nTo show the top functions by time spent, including called functions:\n```shell\n$ poetry run python -m cProfile -s tottime ./duplicate_images/duplicate.py \\ \n    --algorithm $ALGORITHM --action-equal none $IMAGE_DIR 2>&1 | head -n 15\n```\nor, to show the top functions by time spent in the function alone:\n```shell\n$ poetry run python -m cProfile -s cumtime ./duplicate_images/duplicate.py \\ \n    --algorithm $ALGORITHM --action-equal none $IMAGE_DIR 2>&1 | head -n 15\n```\n\n#### Memory usage\n```shell\n$ poetry run fil-profile run ./duplicate_images/duplicate.py \\\n    --algorithm $ALGORITHM --action-equal none $IMAGE_DIR 2>&1\n```\nThis will open a browser window showing the functions using the most memory (see \nhttps://pypi.org/project/filprofiler for more details).',
    'author': 'Lene Preuss',
    'author_email': 'lene.preuss@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lene/DuplicateImages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ghstack']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3,<4',
 'importlib-metadata>=3,<4',
 'requests>=2,<3',
 'typing-extensions>=3,<5']

extras_require = \
{':python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['ghstack = ghstack.__main__:main']}

setup_kwargs = {
    'name': 'ghstack',
    'version': '0.7.0',
    'description': 'Stack diff support for GitHub',
    'long_description': '# ghstack\n\nConveniently submit stacks of diffs to GitHub as separate pull requests.\n\n```\npip3 install ghstack\n```\n\nPython 3.6 and greater only.\n\n## How to setup\n\nGo to github.com `Settings→Developer Settings→Personal Access Tokens` and\ngenerate a token with `public_repo` access only.\nCreate a `~/.ghstackrc` as shown below:\n```\nλ cat ~/.ghstackrc\n[ghstack]\ngithub_url = github.com\ngithub_oauth = [your_own_token]\ngithub_username = [your_username]\nremote_name = upstream [if remote is called upstream and not origin]\n```\n\n## How to use\n\nMake sure you have write permission to the repo you\'re opening PR with.\n\nPrepare a series of commits on top of master, then run `ghstack`.  This\ntool will push and create pull requests for each commit on the stack.\n\n**How do I stack another PR on top of an existing one?** Assuming\nyou\'ve checked out the latest commit from the existing PR, just\n`git commit` a new commit on top, and then run `ghstack`.\n\n**How do I modify a PR?**  Just edit the commit in question, and then\nrun `ghstack` again.  If the commit is at the top of your stack,\nyou can edit it with `git commit --amend`; otherwise, you\'ll have\nto use `git rebase -i` to edit the commit directly.\n\n**How do I rebase?**  The obvious way: `git rebase origin/master`.\nDon\'t do a `git merge`; `ghstack` will throw a hissy fit if you\ndo that.  (There\'s also a more fundamental reason why this\nwon\'t work: since each commit is a separate PR, you have to\nresolve conflicts in *each* PR, not just for the entire stack.)\n\n**How do I start a new feature?**  Just checkout master on a new\nbranch, and start working on a fresh branch.\n\n**WARNING.**  You will NOT be able to merge these commits using the\nnormal GitHub UI, as their branch bases won\'t be master.  Use\n`ghstack land $PR_URL` to land a ghstack\'ed pull request.\n\n## Structure of submitted pull requests\n\nEvery commit in your local commit stack gets submitted into a separate\npull request and pushes commits onto three branches:\n\n* `gh/username/1/base` - think of this like "master": it\'s the base\n  branch that your commit was based upon.  It is never force pushed;\n  whenever you rebase your local stack, we add merge commits on top of\n  base from the true upstream master.\n\n* `gh/username/1/head` - this branch is your change, on top of the base\n  branch.  Like base, it is never force pushed.  We open a pull request\n  on this branch, requesting to merge into base.\n\n* `gh/username/1/orig` - this is the actual commit as per your local\n  copy.  GitHub pull requests never sees this commit, but if you want\n  to get a "clean" commit all by itself, for example, because you\n  want to work on the commits from another machine, this is the best way\n  to get it.\n\n## Developer notes\n\nThis project uses [Poetry](https://python-poetry.org/docs/#installation), so\nafter you\'ve installed Poetry itself, run this command in your clone of this\nrepo to install all the dependencies you need for working on `ghstack`:\n```\npoetry install\n```\nNote that this installs the dependencies (and `ghstack` itself) in an isolated\nPython virtual environment rather than globally. If your cwd is in your clone of\nthis repo then you can run your locally-built `ghstack` using `poetry run\nghstack $ARGS`, but if you want to run it from somewhere else, you probably want\n[`poetry shell`](https://python-poetry.org/docs/cli/#shell) instead:\n```\npoetry shell\ncd $SOMEWHERE\nghstack $ARGS\n```\n\n### Testing\n\nWe have tests, using a mock GitHub GraphQL server!  How cool is that?\n```\npoetry run python test_ghstack.py\n```\nThat runs most of the tests; you can run all tests (including lints) like this:\n```\npoetry run ./run_tests.sh\n```\n\n### Publishing\n\nYou can also [use Poetry to\npublish](https://python-poetry.org/docs/cli/#publish) to a package repository.\nFor instance, if you\'ve configured your [Poetry\nrepositories](https://python-poetry.org/docs/repositories/) like this:\n```\npoetry config repositories.testpypi https://test.pypi.org/legacy/\n```\nThen you can publish to TestPyPI like this:\n```\npoetry publish --build --repository testpypi\n```\nTo publish to PyPI itself, just omit the `--repository` argument.\n\n## Design constraints\n\nThere are some weird aspects about GitHub\'s design which lead to unusual\ndesign decisions on this tool.\n\n1. When you create a PR on GitHub, it is ALWAYS created on the\n   repository that the base branch exists on.  Thus, we MUST\n   push branches to the upstream repository that you want\n   PRs to be created on.  This can result in a lot of stale\n   branches hanging around; you\'ll need to setup some other\n   mechanism for pruning these branches.\n\n2. Branch name does not correspond to pull request number. While this\n   would be excellent, we have no way of reserving a pull request\n   number, so we have no idea what it\'s going to be until we open\n   the pull request, but we can\'t open the pull request without a\n   branch.\n\n## Ripley Cupboard\n\nChanneling Conor McBride, this section documents mistakes worth\nmentioning.\n\n**Non-stack mode.**  ghstack processes your entire stack when it\nuploads updates, but it doesn\'t have to be that way; you could\nimagine that you could ask ghstack to only process the topmost\ncommit and leave the rest alone.  An easy and attractive\nlooking way of doing this is to edit the stack selection algorithm\nto look a single commit, rather than all the commits from\nmerge-base to head.\n\nThis sounds OK but you try it and you realize two things:\n\n1. This is wrong, if you exclude the commits before your commit\n   you\'ll end up with a base commit based on the "literal"\n   commit in your Git repository.  But this has no relationship\n   with the base commit that was previously uploaded, which\n   was synthetically constructed.\n\n2. You also have do extra work to pull out an up to date stack\n   to write into the pull request body.\n\nSo, this is not impossible to do, but it will need some work.\nYou have to work out what the real base commit is, whether\nor not you need to advance it, and also rewrite the stack rendering\ncode.\n',
    'author': 'Edward Z. Yang',
    'author_email': 'ezyang@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ezyang/ghstack',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

"""Collection of tests around repository type identification."""
import pytest

from cookiecutter import exceptions, vcs


@pytest.mark.parametrize(
    'repo_url, exp_repo_type, exp_repo_url',
    [
        (
            'git+https://github.com/pytest-dev/cookiecutter-pytest-plugin.git',
            vcs.Git,
            'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git',
        ),
        (
            'hg+https://bitbucket.org/foo/bar.hg',
            vcs.Hg,
            'https://bitbucket.org/foo/bar.hg',
        ),
        (
            'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git',
            vcs.Git,
            'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git',
        ),
        (
            'https://bitbucket.org/foo/bar.hg',
            vcs.Hg,
            'https://bitbucket.org/foo/bar.hg',
        ),
        (
            'https://github.com/audreyr/cookiecutter-pypackage.git',
            vcs.Git,
            'https://github.com/audreyr/cookiecutter-pypackage.git',
        ),
        (
            'https://github.com/audreyr/cookiecutter-pypackage',
            vcs.Git,
            'https://github.com/audreyr/cookiecutter-pypackage',
        ),
        (
            'git@gitorious.org:cookiecutter-gitorious/cookiecutter-gitorious.git',
            vcs.Git,
            'git@gitorious.org:cookiecutter-gitorious/cookiecutter-gitorious.git',
        ),
        (
            'https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket',
            vcs.Hg,
            'https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket',
        ),
        ('svn+file:///home/johndoe/myrepo', vcs.SVN, 'file:///home/johndoe/myrepo',),
        ('svn+https://private.com/myrepo', vcs.SVN, 'https://private.com/myrepo',),
        ('svn://private.com/myrepo', vcs.SVN, 'svn://private.com/myrepo',),
        ('svn+ssh://private.com/myrepo', vcs.SVN, 'svn+ssh://private.com/myrepo',),
    ],
)
def test_identify_known_repo(repo_url, exp_repo_type, exp_repo_url):
    """Verify different correct repositories url syntax is correctly transformed."""
    assert vcs.identify_repo(repo_url) == (exp_repo_type, exp_repo_url)


@pytest.fixture(
    params=[
        'foo+git',  # uses explicit identifier with 'git' in the wrong place
        'foo+hg',  # uses explicit identifier with 'hg' in the wrong place
        'foo+bar',  # uses explicit identifier with neither 'git' nor 'hg'
        'foobar',  # no identifier but neither 'git' nor 'bitbucket' in url
        'http://norepotypespecified.com',
        'git+svn://private.com/myrepo',
    ]
)
def unknown_repo_type_url(request):
    """Fixture. Return wrong formatted repository url."""
    return request.param


def test_identify_raise_on_unknown_repo(unknown_repo_type_url):
    """Verify different incorrect repositories url syntax trigger error raising."""
    with pytest.raises(exceptions.UnknownRepoType):
        vcs.identify_repo(unknown_repo_type_url)

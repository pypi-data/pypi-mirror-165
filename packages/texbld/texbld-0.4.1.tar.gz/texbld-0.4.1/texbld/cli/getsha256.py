from argparse import ArgumentParser, ArgumentTypeError
from texbld.cli.resource import ImageResource, image_resource_type
from texbld.common.image.image import GitHubImage
from texbld.utils.github import get_github_rev


def getsha256(resource):
    if mch := ImageResource.github_regex.fullmatch(resource):
        # we don't care about the config file here.
        owner, repository, rev, _ = mch.groups()
        rev = rev[1:] if rev is not None and len(rev) > 1 else None
        rev = get_github_rev(owner, repository, rev)
        image = GitHubImage(owner, repository, rev, sha256=None)
        image.client.fetch()
        return (rev, image.client.getsha256())
    else:
        raise ArgumentTypeError(
            f'Error: Resource {resource} is not a GitHub resource.')


def getsha256_cli(args):
    rev, sha256 = getsha256(args.resource)
    print(f"revision: {rev}")
    print(f"sha256: {sha256}")


def add_sha_args(parser: ArgumentParser):
    parser.add_argument('resource', type=image_resource_type,
                        help='GitHub resource to get sha256 of')
    parser.set_defaults(func=getsha256_cli)

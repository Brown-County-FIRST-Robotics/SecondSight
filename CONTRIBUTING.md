# Contributing to SecondSight

If you would like to contribute to this project and want to open a GitHub pull request ("PR"), there are guidelines for patches. Please review this entire document before submitting a pull request.

## Setting up your environment

Before you can contribute to SecondSight, you need to configure your development environment.

### Python Setup

SecondSight is developed using Python. You should configure a virtual environment to ensure you have the correct dependencies and you avoid polluting the global python environment with dependencies.

To create a python virtual environment ensure you have the 'venv' python module installed. For example on Ubuntu you would run `sudo apt-get install -y python3-venv` to install this module.

Then run

```shell
python -m venv secondsight_env
source secondsight_env/bin/activate
```

You must remember to run the `source` command when running or developing for SecondSight.

## Configuring Git

You will need to configure your git client with your name and email address. This is easily done from the command line.

```text
$ git config --global user.name "John Doe"
$ git config --global user.email "john.doe@example.com"
```

This username and email address will matter later in this guide.

## Fork the repo

You should fork the SecondSight repo using the "Fork" button at the top right of the SecondSight GitHub repo. You will develop your patch in your personal fork, then submit a pull request containing your changes. There are many resources how to use GitHub effectively, we will not cover those here.

## Commit guidelines

Please keep commits limited to the feature beign worked on. Commits should not contain spurious changes. The submission should include enough details for a future developer to understand how the bugfix or feature works. Please do not try to be clever in your commit messages. Being to the point is prefered.

## Sign off your work

The `sign-off` is an added line at the end of the explanation for the commit, certifying that you wrote it or otherwise have the right to submit it as an open-source patch. By submitting a contribution, you agree to be bound by the terms of the DCO Version 1.1 and Apache License Version 2.0.

Signing off a commit certifies the below Developer's Certificate of Origin (DCO):

```text
Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

   (a) The contribution was created in whole or in part by me and I
       have the right to submit it under the open source license
       indicated in the file; or

   (b) The contribution is based upon previous work that, to the best
       of my knowledge, is covered under an appropriate open source
       license and I have the right under that license to submit that
       work with modifications, whether created in whole or in part
       by me, under the same open source license (unless I am
       permitted to submit under a different license), as indicated
       in the file; or

   (c) The contribution was provided directly to me by some other
       person who certified (a), (b) or (c) and I have not modified
       it.

   (d) I understand and agree that this project and the contribution
       are public and that a record of the contribution (including all
       personal information I submit with it, including my sign-off) is
       maintained indefinitely and may be redistributed consistent with
       this project or the open source license(s) involved.
```

All contributions to this project are licensed under the [Apache License Version 2.0, January 2004](http://www.apache.org/licenses/).

When committing your change, you can add the required line manually so that it looks like this:

```text
Signed-off-by: John Doe <john.doe@example.com>
```

Creating a signed-off commit is then possible with `-s` or `--signoff`:

```text
$ git commit -s -m "this is a commit message"
```

To double-check that the commit was signed-off, look at the log output:

```text
$ git log -1
commit 37ceh170e4hb283bb73d958f2036ee5k07e7fde7 (HEAD -> issue-35, origin/main, main)
Author: John Doe <john.doe@example.com>
Date:   Mon Aug 1 11:27:13 2020 -0400

    this is a commit message

    Signed-off-by: John Doe <john.doe@example.com>
```

This repository will enforce the DCO, if you forgot to add it to your commits, plese see this
[DCO is missing](https://github.com/src-d/guide/blob/master/developer-community/fix-DCO.md) guide.

## Test your changes

TODO: Add this section later

## Pull Request

If you made it this far and all the tests are passing, it's time to submit a Pull Request (PR) for SecondSight. Submitting a PR is always a scary moment as what happens next can be an unknown. This project strives to be easy to work with, we appreciate all contributions. Nobody is going to yell at you or try to make you feel bad. We love contributions and know how scary that first PR can be, especially if it's your first.

Welcome to our community!

### PR Title and Description

Just like the commit details mentioned above, the PR title and description is very important for letting others know what's happening. Please include any details you think a reviewer will need to more properly review your PR.

A PR that is very large or poorly described has a higher likelihood of being pushed to the end of the list. Reviewers like PRs they can understand and quickly review.

### What to expect next

Please be patient with the project. We try to review PRs in a timely manner, but this is highly dependent on all the other tasks we have going on. It's OK to ask for a status update every week or two, it's not OK to ask for a status update every day.

It's very likely the reviewer will have questions and suggestions for changes to your PR. If your changes don't match the current style and flow of the other code, expect a request to change what you've done.

## Document your changes

And lastly, when proposed changes are modifying user-facing functionality or output, it is expected the PR will include updates to the documentation as well

If nobody knows new features exist, they can't use them!

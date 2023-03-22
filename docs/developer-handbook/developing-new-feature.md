## Git Flow

Currently we have 2 environments, namely `development` and `production`. Development is an environment that all of the implemented features are being tested together, so `development` is almost always ahead of the `production` branch. `production` branch is the stable branch, which is actively being used by real people (not just our QA and Product teams like `Development`) so it should only contain features that have been approved and teste by team. We make deployments feature by feature, every feature should have their own branch which is created from `production`.
More can be found in [Working with Git and GitHub](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/working-with-git/)

### Sample Git Flow

1. Create the feature branch from `production` branch.
  ```git
  git checkout production
  git checkout -b featureName-developerName
  ```
2. You may merge `production` branch to the feature branch any time (for example to resolve conflicts).
  ```git
  git merge origin/production
  ```
3. Implement the feature and move issue to `In Progress` column from [Github board](https://github.com/orgs/swe574-spring23/projects/1).
  ```git
  git add .
  git commit -m "Feature name"
  git push
  ```
4. Create a Pull Request (PR) from your feature branch to `development`, and request a review from other developers.
- Add title as `DEV | Feature name`.
- Add description of the feature.
- Assign your teammates to reviewers.
- Assign the issue to yourself.
- Assign the PR labels which are explained in [labels](https://github.com/swe574-spring23/SWE574/docs/github/labels.md) section.
- Assign project as `SWE574`.
- Assign progress status from the project.
- Mention the issue number in the description.
**If the feature is still work in progress you can create a draftt PR by clicking the down arrow next to `Create pull request`and select `Create a draft pull request`**
5. Go to related issue and select your previous PR for development part from the right sidebar.
6. After the PR is approved by reviwers, merge it and test it on `development`.
7. After your feature branch is merged into `development`, create another PR to `production` from your feature branch. Apply same PR rules as `development` except name it as `PROD | Feature name`.
8. After the PR is tested by other team members, merge it and test it on `production`.
9. After your feature branch is merged into `production`, go to [Github board](https://github.com/orgs/swe574-spring23/projects/1) and move it to `Done`.

More about git commands can be found in [Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)


### Branch Naming Conventions

We use the following naming conventions for branches: `feature-developer`

ex: space-ahmet

### Writing Git Commit Messages

- It should start with a verb in the imperative mood.
- It should be short and descriptive.
- It should be written in English.
- It should be written in the present tense.
- It should be less than 50 characters.(not a must)
- It shouldn't have a period at the end.

ex: `Add a new feature`, `Fix a bug`, `Update the documentation`

More can be found:
- [Writing Git Commit Messages](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/#writing-git-commit-messages)
- [How to Write a Git Commit Message](https://cbea.ms/git-commit/)



### Pull Request Acceptence Criteria
- The linter test should pass.
- All tests should pass.
- The migrations shouldn't have any conflicts.
- The PR should include the tests of the feature.
- The coverage of the project should be more than 80%.
- The PR should work without any bugs, if there any known bugs, they should be mentioned in the PR description.
- The PR should be reviewed by at least one other developer.
- The PR should be tested by at least one other developer.
- The PR should be merged into the correct branch.
- The PR should be assigned to the correct labels.
- The PR should be assigned to the correct milestone.
- The PR should be assigned to the correct assignee.


### Don'ts :no_entry_sign:

- Never merge `development` into your feature branch.
  - `development` branch contains untested and possibly backward incompatible features. By doing so, your feature branch would deploy this changes to `production` at the end of the git flow.
- Again, NEVER merge `development` into your feature branch. :)
- Never merge `development` into `production` branch if there are untested features in `development`.
  - :point_up:
- Never create a feature branch from `development`.
  - :point_up:
- Never push commits directly to `development` or `production` branch, always create PRs and make sure that your PR is reviewed by another developer.
- Never use force-pushes.
  - If anyone else has checked out your branch (say, to review/test your changes), they will have to delete their copy of your branch and re-fetch it from the remote repository.
  - Rebase/force-push can have a tendency to mess up the placement of comments made on your PR in GitHub/Bitbucket — sometimes they will disappear entirely!
  - Any changes that someone else has made to this branch between when you checked it out and now will be obliterated — as though they never happened.
- It's better to let the reviewer resolve conversations, since they should after check what is requested and what is done.


# TODO: review the parts after this

## Testing

### Traditional Django tests
1. Bash to container PROJECT_CONT via `docker-compose exec app bash`
2. `python manage.py test`

**Note**: If you want to run tests with different settings configurations you can use ---settings option for example: `python manage.py --settings=PROJECT.settings.dev test`


### Debugging
With Python 3.7 we have `breakpoint()` available. The default debugger is [`pudb`](https://pypi.org/project/pudb/). To change it set the environment variable `PYTHONBREAKPOINT`. For more info read [this awesome article](https://hackernoon.com/python-3-7s-new-builtin-breakpoint-a-quick-tour-4f1aebc444c).

### Test Coverage
1. Bash to `PROJECT_CONT` container via `docker-compose exec PROJECT_CONT bash`
2. `pip install coverage`
3. `coverage run --source='.' --settings=PROJECT_CONT.settings.testing manage.py test`
4. `coverage html -i` (printing html report)
5. Report is stored generated in `htmlcov/index.html`

## Admin panel
Use `PROJECT_CONT/admin/` for admin panel.



### Project Dependencies
- All project and package dependencies should be included in related files, i.e. [requirements.txt](requirements.txt) or [Dockerfile](python.Dockerfile).
- If you add a new dependency, make sure to update the related files.

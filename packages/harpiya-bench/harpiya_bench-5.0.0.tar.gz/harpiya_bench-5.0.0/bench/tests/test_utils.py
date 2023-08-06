import os
import shutil
import subprocess
import unittest

from bench.app import App
from bench.bench import Bench
from bench.exceptions import InvalidRemoteException
from bench.utils import is_valid_harpiya_branch


class TestUtils(unittest.TestCase):
	def test_app_utils(self):
		git_url = "https://github.com/harpiyacloud/harpiya"
		branch = "develop"
		app = App(name=git_url, branch=branch, bench=Bench("."))
		self.assertTrue(
			all(
				[
					app.name == git_url,
					app.branch == branch,
					app.tag == branch,
					app.is_url is True,
					app.on_disk is False,
					app.org == "harpiyacloud",
					app.url == git_url,
				]
			)
		)

	def test_is_valid_harpiya_branch(self):
		with self.assertRaises(InvalidRemoteException):
			is_valid_harpiya_branch(
				"https://github.com/harpiyacloud/harpiya.git", harpiya_branch="random-branch"
			)
			is_valid_harpiya_branch(
				"https://github.com/random/random.git", harpiya_branch="random-branch"
			)

		is_valid_harpiya_branch(
			"https://github.com/harpiyacloud/harpiya.git", harpiya_branch="develop"
		)
		is_valid_harpiya_branch(
			"https://github.com/harpiyacloud/harpiya.git", harpiya_branch="v13.29.0"
		)

	def test_app_states(self):
		bench_dir = "./sandbox"
		sites_dir = os.path.join(bench_dir, "sites")

		if not os.path.exists(sites_dir):
			os.makedirs(sites_dir)

		fake_bench = Bench(bench_dir)

		self.assertTrue(hasattr(fake_bench.apps, "states"))

		fake_bench.apps.states = {
			"harpiya": {
				"resolution": {"branch": "develop", "commit_hash": "234rwefd"},
				"version": "14.0.0-dev",
			}
		}
		fake_bench.apps.update_apps_states()

		self.assertEqual(fake_bench.apps.states, {})

		harpiya_path = os.path.join(bench_dir, "apps", "harpiya")

		os.makedirs(os.path.join(harpiya_path, "harpiya"))

		subprocess.run(["git", "init"], cwd=harpiya_path, capture_output=True, check=True)

		with open(os.path.join(harpiya_path, "harpiya", "__init__.py"), "w+") as f:
			f.write("__version__ = '11.0'")

		subprocess.run(["git", "add", "."], cwd=harpiya_path, capture_output=True, check=True)
		subprocess.run(
			["git", "config", "user.email", "bench-test_app_states@gha.com"],
			cwd=harpiya_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "config", "user.name", "App States Test"],
			cwd=harpiya_path,
			capture_output=True,
			check=True,
		)
		subprocess.run(
			["git", "commit", "-m", "temp"], cwd=harpiya_path, capture_output=True, check=True
		)

		fake_bench.apps.update_apps_states(app_name="harpiya")

		self.assertIn("harpiya", fake_bench.apps.states)
		self.assertIn("version", fake_bench.apps.states["harpiya"])
		self.assertEqual("11.0", fake_bench.apps.states["harpiya"]["version"])

		shutil.rmtree(bench_dir)

	def test_ssh_ports(self):
		app = App("git@github.com:22:harpiyacloud/harpiya")
		self.assertEqual((app.use_ssh, app.org, app.repo), (True, "harpiyacloud", "harpiya"))

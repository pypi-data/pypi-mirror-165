VERSION = "5.2.0"
PROJECT_NAME = "harpiya-bench"
HARPIYA_VERSION = None
current_path = None
updated_path = None
LOG_BUFFER = []


def set_harpiya_version(bench_path="."):
	from .utils.app import get_current_harpiya_version

	global HARPIYA_VERSION
	if not HARPIYA_VERSION:
		HARPIYA_VERSION = get_current_harpiya_version(bench_path=bench_path)

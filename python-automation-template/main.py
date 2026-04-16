import argparse
import getpass
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

import tomllib

from services.logging import LoggerService
from services.notification import Notification

# GLOBAL CONSTANTS
PROJECT_ROOT = Path(__file__).resolve().parent


def process_data_temporarily():
    """
    This creates a safe, unique folder (e.g., /tmp/tmp_8x2a9d/)
    It automatically cleans itself up when the "with" block ends
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        safe_temp_path = Path(temp_dir)
        # Download anything and process anythings inside the tmp folder

        temp_file = safe_temp_path / "tmp.txt"
        # Do your processing here...

    print("Temporary folder deleted automatically.")


def generate_unique_filename(prefix, extension, env, logger):
    """
    Example output: log_20260416_153000_msharathh.csv
    Example output: dev_log_20260416_153000_msharathh.csv
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    user = getpass.getuser()
    env_str = f"{env}_" if env else ""
    clean_ext = extension if extension.startswith(".") else f".{extension}"

    final_name = f"{env_str}{prefix}_{timestamp}_{user}{clean_ext}"

    return final_name


def parse_cli_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Automation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py --env dev
        """,
    )

    parser.add_argument(
        "--env",
        type=str,
        required=True,
        choices=["dev", "staging", "prod"],
        help="Environment to run (dev, staging, prod)",
    )

    parser.add_argument(
        "--path",
        type=str,
        nargs="+",  # This makes it accept one or more values as a list
        required=False,
        default=[],
        help="One or more file/directory paths (space separated)",
    )

    return parser.parse_args()


def load_config(env):
    """Load configuration from TOML file"""
    config_path = PROJECT_ROOT / "config.toml"

    with open(config_path, "rb") as f:
        full_config = tomllib.load(f)  # Dict output

    # Start with default config
    config = full_config.get("default", {}).copy()

    # Override with environment config
    env_config = full_config.get(env, {})
    config.update(env_config)  # default + env specific config

    # Add environment name to config
    config["environment"] = env

    return config


def usage_example(config, args, logger):
    logger.debug(f"Starting automation in {args.env} environment")
    logger.info(f"Starting automation in {args.env} environment")
    logger.warning(f"Starting automation in {args.env} environment")
    logger.error(f"Starting automation in {args.env} environment")
    print(f"config: {config}")
    print(f"args: {args.env}")
    return True


def logic(logger, notification):
    logger.info("Executing second logic")

    # Send success notification
    notification.send_email(
        subject="Task Complete", body="All tasks processed successfully"
    )

    called_by_other()

    return True


def called_by_other():
    print("This function called by other function")


def run_cmd(cmd, logger):
    try:
        # Get a safe copy of current variables
        child_env = os.environ.copy()

        # Inject specific `export` variable only into new variable just for the child process; otherwise all
        child_env["ENV"] = "$ENV"

        logger.info(f"Running the Command: {cmd}")
        shell_output = subprocess.run([cmd], env=child_env, shell=True, text=True)
        return shell_output.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {cmd} - Error: {e}")
        return ""


def main():
    # CLI arguments
    args = parse_cli_args()
    print(f"Running with environment: {args.env}")

    # Load configuration based on environment
    config = load_config(args.env)
    print(config["database"])
    print(args.path)

    # Initialize service
    log_output_dir = PROJECT_ROOT / "outs" / "logs"
    logger = LoggerService(config["log_level"], log_output_dir)

    notification = Notification(config, logger)

    # Calling main logics functions
    usage_example(config, args, logger)
    logic(logger, notification)  # Pass the notification services as args

    logger.info("Automation completed successfully")


if __name__ == "__main__":
    main()

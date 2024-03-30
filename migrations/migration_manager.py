import modules.logs as logging

from migrations.m001_env_var_to_config_yaml import Migration as Migration001


class MigrationManager:
    def __init__(self, config_directory: str, logs_directory: str):
        self.config_directory = config_directory
        self.logs_directory = logs_directory

        self.migrations = [
            # Copy environment variables to a YAML file (not config.yaml to avoid schema issues)
            Migration001(number="001", migration_tracker_folder=self.config_directory,
                         config_folder=self.config_directory,
                         logs_folder=self.logs_directory),
        ]

    def run_migrations(self) -> bool:
        for migration in self.migrations:
            try:
                if not migration.pre_forward_check():
                    logging.info(f"Migration {migration.number} skipped")
                    continue

                migration.forward()

                if not migration.post_forward_check():
                    logging.error(f"Migration {migration.number} failed")
                    return False  # Exit early, prevent further migrations

                migration.mark_done()
            except Exception as e:
                logging.error(f"Migration {migration.number} failed: {e}")
                return False  # Exit early, prevent further migrations

        return True
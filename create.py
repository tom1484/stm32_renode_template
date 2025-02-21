import argparse
import os
import shutil
import json5

def merge_json_files(source_path, dest_path, replacements):
    """Merge source JSON5 into destination JSON5 file, applying replacements."""
    try:
        # Read source JSON5
        with open(source_path, 'r') as f:
            source_content = f.read()
        
        # Apply replacements to source content
        for tag, value in replacements.items():
            source_content = source_content.replace(f'<{tag}>', value)
        
        # Parse source JSON5
        source_json = json5.loads(source_content)

        # Read destination JSON5 if it exists, otherwise use empty dict
        dest_json = {}
        if os.path.exists(dest_path):
            with open(dest_path, 'r') as f:
                dest_json = json5.load(f)

        # Merge configurations
        if 'configurations' in source_json:
            if 'configurations' not in dest_json:
                dest_json['configurations'] = []
            
            # Update or add each configuration
            for src_config in source_json['configurations']:
                # Find matching configuration by name
                dest_config = next(
                    (cfg for cfg in dest_json['configurations'] 
                     if cfg.get('name') == src_config.get('name')), 
                    None
                )
                if dest_config:
                    # Update existing configuration
                    dest_config.update(src_config)
                else:
                    # Add new configuration
                    dest_json['configurations'].append(src_config)

        # Merge tasks
        if 'tasks' in source_json:
            if 'tasks' not in dest_json:
                dest_json['tasks'] = []
            
            # Update or add each task
            for src_task in source_json['tasks']:
                # Find matching task by label
                dest_task = next(
                    (task for task in dest_json['tasks'] 
                     if task.get('label') == src_task.get('label')), 
                    None
                )
                if dest_task:
                    # Update existing task
                    dest_task.update(src_task)
                else:
                    # Add new task
                    dest_json['tasks'].append(src_task)

        # Write merged JSON with standard VS Code comment
        with open(dest_path, 'w') as f:
            f.write('// Configuration file managed by Renode setup script\n')
            json5.dump(dest_json, f, indent=4, quote_keys=True)
            
        print(f"Merged configuration into {dest_path}")
    except Exception as e:
        print(f"Error merging JSON5 file {dest_path}: {e}")

def copy_config_files(source_dir, dest_dir, replacements):
    """Copy and merge configuration files to target project."""
    try:
        # Handle .vscode directory
        vscode_src = os.path.join(source_dir, '.vscode')
        vscode_dest = os.path.join(dest_dir, '.vscode')
        os.makedirs(vscode_dest, exist_ok=True)

        # Merge JSON files
        for json_file in ['launch.json', 'tasks.json']:
            src_path = os.path.join(vscode_src, json_file)
            dest_path = os.path.join(vscode_dest, json_file)
            if os.path.exists(src_path):
                merge_json_files(src_path, dest_path, replacements)

        # Copy renode directory
        renode_src = os.path.join(source_dir, 'renode')
        renode_dest = os.path.join(dest_dir, 'renode')
        if os.path.exists(renode_src):
            if os.path.exists(renode_dest):
                shutil.rmtree(renode_dest)
            shutil.copytree(renode_src, renode_dest)
            print(f"Copied renode to {renode_dest}")

    except Exception as e:
        print(f"Error copying configuration files: {e}")
        raise

def replace_in_file(file_path, replacements):
    """Replace tags in a file with their corresponding values."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        for tag, value in replacements.items():
            content = content.replace(f'<{tag}>', value)

        with open(file_path, 'w') as f:
            f.write(content)
            
        print(f"Updated {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def process_directory(directory, replacements):
    """Process all files in directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.resc', '.repl')):  # Only process renode config files
                file_path = os.path.join(root, file)
                replace_in_file(file_path, replacements)

def main():
    parser = argparse.ArgumentParser(description='Configure Renode development environment')
    parser.add_argument('--project-path', required=True,
                      help='Path to target project directory')
    parser.add_argument('--cpu', required=True,
                      help='CPU name')
    parser.add_argument('--board', required=True,
                      help='Board name (e.g., STM32F429ZITx)')
    parser.add_argument('--remote-user', required=True,
                      help='Remote user name')
    parser.add_argument('--remote-host', required=True,
                      help='Remote host address')
    parser.add_argument('--gdb-port', required=True,
                      help='GDB target port')

    args = parser.parse_args()

    # Get project name from project path
    project_name = os.path.basename(os.path.normpath(args.project_path))

    # Create target project directory if it doesn't exist
    os.makedirs(args.project_path, exist_ok=True)

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create replacements dictionary
    replacements = {
        'CPU': args.cpu,
        'CPU_SVD': args.cpu.upper(),
        'BOARD_NAME': args.board,
        'MACH_NAME': args.board,  # MACH_NAME uses the same value as BOARD_NAME
        'PROJECT_NAME': project_name,
        'REMOTE_USER': args.remote_user,
        'REMOTE_HOST': f'{args.remote_user}@{args.remote_host}',
        'GDB_PORT': args.gdb_port,
        'GDB_TARGET': f'{args.remote_host}:{args.gdb_port}'
    }

    # Copy configuration files to project directory
    copy_config_files(script_dir, args.project_path, replacements)

    # Process .vscode directory in target project
    vscode_dir = os.path.join(args.project_path, '.vscode')
    if os.path.exists(vscode_dir):
        process_directory(vscode_dir, replacements)

    # Process renode directory in target project
    renode_dir = os.path.join(args.project_path, 'renode')
    if os.path.exists(renode_dir):
        process_directory(renode_dir, replacements)

if __name__ == '__main__':
    main()


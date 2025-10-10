"""
Main entry point for NHL data processing
"""

import sys
from registry import (
    get_command,
    list_available_commands,
    register_module_commands,
    print_help
)

def perform_debug_action(args=[]):
    action = "get"
    method = "games"

    try:
        cmd = get_command(action, method)
        (results, printer, header) = cmd(args[2:])
        if header: header()
        if printer: printer()
        else: print(results)
        print("✅ Success!")
    except Exception as e:
        print(f"❌ Error executing command '{action} {method}': {e}")
    except SystemExit as e:
        if e.code == 0:
            pass
        elif e.code == 1:
            print(f"❌ Unknown command '{action} {method}' was entered. Please try again.")
        else:
            print(f"❌ {action.capitalize()} {method} exited!\n   {e}")
    return
...

# Import modules that contain commands
import actions

# Ensure all commands are registered
register_module_commands(actions)

if __name__== "__main__":
    if hasattr(sys, "orig_argv") and any("debugpy" in arg for arg in sys.orig_argv):
        perform_debug_action(sys.argv)
    else:
        try:
            
            if '-h' in sys.argv or '--help' in sys.argv:
                help_args = [arg for arg in sys.argv[1:] if arg not in ['-h', '--help']]
                print_help(help_args)
                sys.exit(0)
            
            if sys.argv and len(sys.argv) < 3:
                print("❓ Please specify which action you wish to perform")
                print_help([])
                sys.exit(0)

            action = sys.argv[1].lower()
            method = sys.argv[2].lower()
            raw_args = sys.argv[3:]

            # Get the command function dynamically
            command_function = get_command(action, method)

            if not command_function:
                print(f"❌ Unknown command '{action} {method}'")
                print("💡 Available commands:")
                available_commands = list_available_commands()
                for cmd, sub_cmds in available_commands.items():
                    print(f"   {cmd}: [{', '.join(sub_cmds)}]")
                sys.exit(0)
        
            (results, printer, header) = command_function(raw_args)
            print("✅ Success!")
            
            if header: header()
            if printer: printer()
            else: print(results)
        except Exception as e:
            print(f"❌ Error executing command '{action} {method}': {e}")
        except SystemExit as e:
            if e.code == 0:
                pass
            elif e.code == 1:
                print(f"❌ Unknown command '{action} {method}' was entered. Please try again.")
            else:
                print(f"❌ {action.capitalize()} {method} exited!\n   {e}")
...
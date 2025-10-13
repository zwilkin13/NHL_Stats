"""
Command Registry System
Provides decorators and utilities for automatically registering API commands
"""

from collections import defaultdict

# Global command registry
_COMMAND_REGISTRY = {}
def command(action, method, help_text=None, addtl_help_text=None, 
            args_help=None, options_help=None, print_title=None):
    def decorator(func):
        command_key = f"{action}.{method}"
        _COMMAND_REGISTRY[command_key] = func
        
        # Add metadata to the function for introspection
        func._command_action = action
        func._command_method = method
        func._command_help_text = help_text
        func._command_addtl_help_text = addtl_help_text
        func._command_args_help = args_help
        func._command_options_help = options_help
        func._command_print_title = print_title

        return func
    return decorator
...

def get_command(action, method):
    command_key = f"{action}.{method}"
    return _COMMAND_REGISTRY.get(command_key)
...

def get_all_commands():
    return _COMMAND_REGISTRY.copy()
...

def get_command_help(action, method):
    command_key = f"{action}.{method}"
    if command_key in _COMMAND_REGISTRY:
        func = _COMMAND_REGISTRY[command_key]
        return getattr(func, '_command_help_text', None)
    return None
...

def get_command_addtl_help(action, method):
    command_key = f"{action}.{method}"
    if command_key in _COMMAND_REGISTRY:
        func = _COMMAND_REGISTRY[command_key]
        return getattr(func, '_command_addtl_help_text', None)
    return None
...

def get_command_args_help(action, method):
    command_key = f"{action}.{method}"
    if command_key in _COMMAND_REGISTRY:
        func = _COMMAND_REGISTRY[command_key]
        return getattr(func, '_command_args_help', None)
    return None
...

def get_command_options_help(action, method):
    command_key = f"{action}.{method}"
    if command_key in _COMMAND_REGISTRY:
        func = _COMMAND_REGISTRY[command_key]
        return getattr(func, '_command_options_help', None)
    return None
...

def get_command_print_title(action, method):
    command_key = f"{action}.{method}"
    if command_key in _COMMAND_REGISTRY:
        func = _COMMAND_REGISTRY[command_key]
        return getattr(func, '_command_print_title', None)
    return None
...

def get_all_help():
    help_info = defaultdict(dict)
    for command_key, func in _COMMAND_REGISTRY.items():
        action, method = command_key.split('.', 1)
        help_text = getattr(func, '_command_help_text', 'No description available')
        help_info[action][method] = help_text
    return dict(help_info)
...

def print_help(args=None):
    if not args:
        # General help
        help_info = get_all_help()
        print("\n🚀 NHL Stats - Available Commands:")
        print("=" * 40)
        
        for action_name, methods in help_info.items():
            print(f"\n� {action_name.upper()}:")
            for method, help_text in methods.items():
                print(f"   {action_name} {method:<12} - {help_text}")
        
        print(f"\n💡 Usage: nhl <action> <method> [arguments] [options...]")
        print(f"\n📖 For specific help: nhl <action> <method> -h")
        
    elif len(args) >= 2:
        # Specific command help
        action = args[0].lower()
        method = args[1].lower()
        addtl_help_text = get_command_addtl_help(action, method)
        help_text = get_command_help(action, method)
        args_help = get_command_args_help(action, method)
        options_help = get_command_options_help(action, method)
        
        if help_text:
            print(f"\n📖 Help for '{action} {method}':")
            print(f"   {help_text}")
            if addtl_help_text:
                print(f"   {addtl_help_text}")
            
            usage_args = args_help if args_help else ""
            print(f"\n💡 Usage: nhl {action} {method} {usage_args}")
            if options_help:
                print(f"\n🔧 Options:")
                for option in options_help:
                    print(f"   {option}")
        else:
            print(f"❌ No help available for '{action} {method}'")
    
    elif len(args) == 1:
        # Action-level help
        action = args[0].lower()
        help_info = get_all_help()
        if action in help_info:
            print(f"\n� Available '{action}' commands:")
            for method, help_text in help_info[action].items():
                print(f"   {action} {method:<12} - {help_text}")
            print(f"\n💡 For specific help: nhl {action} <method> -h")
        else:
            print(f"❌ No commands available for action '{action}'")
            # Show available actions
            print(f"ℹ️ Available actions: {', '.join(help_info.keys())}")
...

def list_available_commands():
    grouped = defaultdict(list)
    for key in _COMMAND_REGISTRY.keys():
        action, method = key.split('.', 1)
        grouped[action].append(method)
    return dict(grouped)
...

def register_module_commands(module):
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if callable(attr) and hasattr(attr, '_command_action'):
            # Re-register the command (decorator already did this, but just in case)
            command_key = f"{attr._command_action}.{attr._command_method}"
            _COMMAND_REGISTRY[command_key] = attr
...

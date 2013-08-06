import sublime
import sublime_plugin


class CopyPhpSniffer:
    def __init__(self, view):
        self.view = view

    def find(self, expression):
        expression = '(?<=' + expression + '\s)([a-z]|\\\\)*'
        region = self.view.find(expression, 0, sublime.IGNORECASE)
        print(region, expression)
        if region is not None and region.empty() is False:
            result = self.view.substr(region)
            if result is not False:
                return result.strip()

        return False


class CopyNamespaceCommand(sublime_plugin.WindowCommand):
    def run(self):
        sublime.set_clipboard('')
        sniffer = CopyPhpSniffer(self.window.active_view())
        namespace = sniffer.find('namespace')
        if namespace is not False:
            sublime.set_clipboard(namespace)
            sublime.status_message('Copied namespace: ' + namespace)
        else:
            sublime.error_message('Could not find a namespace')


class CopyClassnameCommand(sublime_plugin.WindowCommand):
    def run(self, with_namespace=False):
        sublime.set_clipboard('')
        sniffer = CopyPhpSniffer(self.window.active_view())
        prefix = ''
        if with_namespace is True:
            namespace = sniffer.find('namespace')
            if namespace is not False:
                prefix = namespace + '\\'

        for option in ['^abstract\sclass', '^class', '^final\sclass' '^interface', '^trait']:
            result = sniffer.find(option)
            print(result)
            if result is not False:
                sublime.set_clipboard(prefix + result)
                sublime.status_message('Copied ' + option + ': ' + prefix + result)
                break

        if result is False:
            sublime.error_message('Could not find a class, interface or trait.')

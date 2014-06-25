import ansible.utils as utils
import ansible.errors as errors

def flatten(terms, facts):
    keys = []

    if facts['ansible_distribution']:
        if facts['ansible_distribution_version']:
            keys.append(facts['ansible_distribution'] + '-' + facts['ansible_distribution_version'])
        if facts['ansible_distribution_major_version']:
            keys.append(facts['ansible_distribution'] + '-' + facts['ansible_distribution_major_version'])
        if facts['ansible_distribution_release']:
            keys.append(facts['ansible_distribution'] + '-' + facts['ansible_distribution_release'])
        keys.append(facts['ansible_distribution'])

    if facts['ansible_os_family']:
        keys.append(facts['ansible_os_family'])

    ret = []
    for term in terms:
        if isinstance(term, str):
            ret.append(term)
        elif isinstance(term, dict):
            for key in keys:
                if key in term:
                    ret.append(term[key])
                    break
            else:
                if 'default' in term:
                    ret.append(term['default'])
    return ret

class LookupModule(object):

    def __init__(self, basedir=None, **kwargs):
        self.basedir = basedir

    def run(self, terms, inject=None, **kwargs):
        terms = utils.listify_lookup_plugin_terms(terms, self.basedir, inject)

        if not isinstance(terms, list):
            raise errors.AnsibleError("with_os_specific expects a list")

        return flatten(terms, inject)

#!/usr/bin/env python
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import ansible.constants 
 
 
class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
 
    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result
 
    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result
 
    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result
 
 
class AnsibleApi(object):
    def __init__(self,resource):
        self.Options = namedtuple('Options',
                             ['connection',
                              'remote_user',
                              'ask_sudo_pass',
                              'verbosity',
                              'ack_pass',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'check',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'sudo_user',
                              'sudo',
                              'diff'])
        
        self.ops = self.Options(connection='ssh',
                              remote_user=None,
                              ask_sudo_pass=False,
                              verbosity=5,
                              ack_pass=None,
                              module_path=None,
                              forks=8,
                              become=None,
                              become_method=None,
                              become_user=None,
                              check=False,
                              listhosts=None,
                              listtasks=None,
                              listtags=None,
                              syntax=None,
                              sudo_user=None,
                              sudo=None,
                              diff=False)
        self.resource = resource
        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=self.resource)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
 
    def runansible(self,host_list, module_name, module_args):
 
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
 
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.ops,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
                run_additional_callbacks=ansible.constants.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(ansible.constants.DEFAULT_LOCAL_TMP, True)


    def get_result(self):
        self.results_raw = {'success':{}, 'failed':{}, 'unreachable':{}}
        for host, result in self.results_callback.host_ok.items():
            self.results_raw['success'][host] = result._result
        for host, result in self.results_callback.host_failed.items():
            self.results_raw['failed'][host] = result._result['msg']
        for host, result in self.results_callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result['msg']
        return self.results_raw
 
 
    def playbookrun(self, playbook_path):
 
        self.variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes'}
        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.ops, passwords=self.passwords)
        result = playbook.run()
        return result
 
 
if __name__ != "__main__":
     pass

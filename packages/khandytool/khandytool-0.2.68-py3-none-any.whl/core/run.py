import click
from core.bladeTest.interactive_tslbusiness import businessProcess
from core.bladeTest.interactive_jmeter import jmeterScriptGen
from core.bladeTest.interactive_testUtil import toolGeter,kafkaListener,mqttListener
from core.bladeTest.interactive_xmind import uploadXmind
from core.bladeTest.interactive import myapp2
from pywebio import start_server
optionDict={
    "bp":"businessProcess",
    "jmeter":"jmeterScriptGen",
    "kafka":"kafkaListener",
    "mqtt":"mqttListener",
    "xmind":"uploadXmind",
    "tool":"toolGeter",
    "all":"myapp2"
    }   

@click.command()
@click.option('--module',default='bp',help='default run business module, other option is all,bp,jmeter,kafka,mqtt,xmind,tool',type=click.Choice(['bp','jmeter','kafka','mqtt','xmind','tool','all']))
def command_run(module):
    start_server(eval(optionDict[module]),port=8999,debug=True,cdn=False,static_hash_cache=False,reconnect_timeout=3600,max_payload_size='500M')

# if __name__=="__main__":
#     command_run()

command_run()
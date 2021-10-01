#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call


def myNetwork():
    net = Mininet(topo=None,
                  build=False,
                  link=TCLink)

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           ip='10.10.10.10',
                           protocol='tcp',
                           port=6634)
//start topology building here

    info('*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    server = net.addHost('server', cls=Host, ip='192.168.0.1/24', netmask='192.168.0.255', defaultRoute=None)
    c1 = net.addHost('c1', cls=Host, ip='10.1.2.1/24', netmask='10.1.1.255', defaultRoute=None)

    info('*** Add links\n')
    linkopts = dict(bw=100, delay='1ms', loss=0, max_queue_size=1000, use_htb=True)
    net.addLink(s1, server, **linkopts)
    net.addLink(s1, c1, **linkopts)

    info('\n*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s1').start([c0])

    info('\n*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()

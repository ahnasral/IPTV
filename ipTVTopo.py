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

    info('*** Add switches\n')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    info('*** Add hosts\n')
    c4 = net.addHost('c4', cls=Host, ip='10.1.2.2/24', netmask='10.1.2.255', defaultRoute=None)
    Server = net.addHost('Server', cls=Host, ip='192.168.0.1', netmask='192.168.0.255', defaultRoute=None)
    c3 = net.addHost('c3', cls=Host, ip='10.1.2.1/24', netmask='10.1.2.255', defaultRoute=None)
    c5 = net.addHost('c5', cls=Host, ip='10.1.3.1/24', netmask='10.1.3.255', defaultRoute=None)
    c1 = net.addHost('c1', cls=Host, ip='10.1.1.1/24', netmask='10.1.1.255', defaultRoute=None)
    c6 = net.addHost('c6', cls=Host, ip='10.1.3.2/24', netmask='10.1.3.255', defaultRoute=None)
    c2 = net.addHost('c2', cls=Host, ip='10.1.1.2/24', netmask='10.1.1.255', defaultRoute=None)

    info('*** Add links\n')
    linkopts = dict(bw=100, delay='1ms', loss=0, max_queue_size=1000, use_htb=True)
    net.addLink(s5, c5, **linkopts)
    net.addLink(s5, c6, **linkopts)
    net.addLink(s4, c3, **linkopts)
    net.addLink(s4, c4, **linkopts)
    net.addLink(s1, Server, **linkopts)
    net.addLink(s3, c1, **linkopts)
    net.addLink(s3, c2, **linkopts)
    net.addLink(s1, s3, **linkopts)
    net.addLink(s1, s4, **linkopts)
    net.addLink(s4, s3, **linkopts)
    net.addLink(s1, s2, **linkopts)
    net.addLink(s4, s2, **linkopts)
    net.addLink(s2, s5, **linkopts)
    net.addLink(s5, s4, **linkopts)

    info('*** Starting network\n')
    net.build()
    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    net.get('s4').start([c0])
    net.get('s2').start([c0])
    net.get('s5').start([c0])
    net.get('s3').start([c0])
    net.get('s1').start([c0])

    info('*** Post configure switches and hosts\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()

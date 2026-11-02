text

```
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
service password-encryption
!
hostname Core-Switch-01
!
username admin privilege 15 password 0 cisco123
!
ip routing
!
ip domain-name lab.local
!
ip http server
ip http secure-server
!
interface FastEthernet0/1
 description User Access Port
 switchport mode access
 switchport access vlan 10
!
interface Vlan1
 description Management Interface
 ip address 192.168.1.250 255.255.255.0
 no shutdown
!
snmp-server community public RO
snmp-server community private RW
!
line vty 0 4
 password 0 password123
 login
 transport input telnet ssh
!
! (no vstack command is missing)
!
end
```
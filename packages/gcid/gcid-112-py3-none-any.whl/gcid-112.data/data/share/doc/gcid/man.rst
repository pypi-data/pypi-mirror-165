.. _man:

.. raw:: html

     <br><br>

.. title:: manual

.. raw:: html

    <center><b>

manual
======

.. raw:: html

    </b></center>
    <br>



**NAME**

 **GENOCIDE** - Prosecutor. Court. Reconsider OTP-CR-117/19.


**SYNOPSIS**

 | ``genocidectl <cmd> [key=value] [key==value]``


**DESCRIPTION**

 **GENOCIDE** holds evidence that king netherlands is doing a genocide, a 
 written :ref:`response <guilty>` where king netherlands confirmed taking note
 of “what i have written”, namely :ref:`proof <evidence>` that medicine he
 uses in treatement laws like zyprexa, haldol, abilify and clozapine are poison
 that make impotent, is both physical (contracted muscles) and mental (let 
 people hallucinate) torture and kills members of the victim groups. 

 **GENOCIDE** contains :ref:`correspondence <writings>` with the
 International Criminal Court, asking for arrest of the king of the 
 netherlands, for the genocide he is committing with his new treatement laws.
 Current status is an outside the jurisdiction judgement of the prosecutor 
 which requires a :ref:`reconsider <reconsider>` to have the king actually
 arrested.

 **GENOCIDE** is a solid, non hackable bot, that runs under systemd as a 
 24/7 background service starts after reboot and is intended to be programmable
 in a static, only code, no popen, no user imports and no reading modules from
 a directory, way. It can show genocide and suicide stats of king netherlands
 his genocide into a IRC channel, display rss feeds and log simple text
 messages, source is :ref:`here <source>`.

**INSTALL**

  | ``sudo pip3 install genocide --upgrade --force-reinstall``


**CONFIGURATION**

 use sudo, ``genocidectl`` needs root privileges

 **irc**

  | ``genocidectl cfg server=<server> channel=<channel> nick=<nick>``
  
  | ``(*) default channel/server is #genocide on localhost``

 **sasl**

  | ``genocidectl pwd <nickservnick> <nickservpass>``
  | ``genocidectl cfg password=<outputfrompwd>``

 **users**

  | ``genocidectl cfg users=True``
  | ``genocidectl met <userhost>``

 **rss**

  | ``genocidectl rss <url>``

 **24/7**

  | ``cp /usr/local/share/genocide/genocide.service /etc/systemd/system``
  | ``systemctl enable genocide --now``


**COMMANDS**

 ::

  cmd - commands
  cfg - irc configuration
  dlt - remove a user
  dpl - sets display items
  ftc - runs a fetching batch
  fnd - find objects 
  flt - list of instances registered to the bus
  log - log some text
  mdl - genocide model
  met - add a user
  mre - displays cached output, channel wise.
  nck - changes nick on irc
  now - genocide stats
  pwd - combines nickserv name/password into a sasl password
  rem - removes a rss feed
  req - request to the prosecutor
  rss - add a feed
  slg - slogan
  thr - show the running threads
  tpc - put genocide stats into topic
  trt - torture definition


**FILES**


 | ``/usr/local/share/doc/genocide/*``
 | ``/usr/local/share/genocide/genocide.service``


**AUTHOR**

 Bart Thate 

**COPYRIGHT**

 **GENOCIDE** is placed in the Public Domain. No Copyright, No License.

.. raw:: html

    <br>
    <center><b>

:ref:`home <home>` - :ref:`manual <man>` - :ref:`source <source>` - :ref:`about <about>`

.. raw:: html

     </b></center>

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 11:30:17 2016

Command Flags panel - contains list of command flags/parameters

Default usage - kept hidden from sidebar. 

"""

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

from wx.lib.pubsub import setupkwargs
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub

from base import *
import subprocess

CMDFLAGS = [
# General Options:
("--config file", "Read configuration options from file."),
("--help", "Show options."),
("--version", "Show copyright and version information."),
# Tunnel Options:
("--local host ", "Local host name or ip address. Implies --bind."),
("--remote host [port] ", "Remote host name or ip address."),
("--remote-random ", "If multiple --remote options specified, choose one randomly."),
("--remote-random-hostname ", "Add a random string to remote DNS name."),
("--mode m ", "Major mode, m = 'p2p' (default, point-to-point) or 'server'."),
("--proto p ", "Use protocol p for communicating with peer. p = udp (default), tcp-server, or tcp-client"),
("--proto-force p ", "only consider protocol p in list of connection profiles. "
                   + "p = udp6, tcp6-server, or tcp6-client (ipv6)"),
("--connect-retry n ", "For --proto tcp-client, number of seconds to wait between connection retries (default=5)."),
("--connect-timeout n ", "For --proto tcp-client, connection timeout (in seconds)."),
("--connect-retry-max n ", "Maximum connection attempt retries, default infinite."),
("--http-proxy s p [up] [auth] ", "Connect to remote host through an HTTP proxy at address s and port p."
                                + "If proxy authentication is required, up is a file containing "
                                + "username/password on 2 lines, or 'stdin' to prompt from console. "
                                + "Add auth='ntlm' if the proxy requires NTLM authentication."),
("--http-proxy s p 'auto[-nct]'", "Like the above directive, but automatically determine auth method "
                                + "and query for username/password if needed.  auto-nct disables weak proxy "
                                + "auth methods."),
("--http-proxy-retry", "Retry indefinitely on HTTP proxy errors."),
("--http-proxy-timeout n ", "Proxy timeout in seconds, default=5."),
("--http-proxy-option type [parm] ", "Set extended HTTP proxy options. Repeat to set multiple options."                           
                                   + "VERSION version (default=1.0)"
                                   + "AGENT user-agent"),
("--socks-proxy s [p] [up] ", "Connect to remote host through a Socks5 proxy at address s and port p "
                            + "(default port = 1080). If proxy authentication is required,"
                            + "up is a file containing username/password on 2 lines, or 'stdin' to prompt for console."),
("--socks-proxy-retry ", "Retry indefinitely on Socks proxy errors."),
("--resolv-retry n", "If hostname resolve fails for --remote, retry resolve for n seconds before failing (disabled by default)."
                   + "Set n='infinite' to retry indefinitely."),
("--float", "Allow remote to change its IP address/port, such as through DHCP (this is the default if --remote is not used)."),
("--ipchange cmd  ", "Run command cmd on remote ip address initialsetting or change -- execute as"
                   + "cmd ip-address port#"),
("--port port  ", "TCP/UDP port # for both local and remote."),
("--lport port ", "TCP/UDP port # for local (default=1194). Implies --bind."),
("--rport port ", "TCP/UDP port # for remote (default=1194)."),
("--bind ", "Bind to local address and port. (This is the default unless--proto tcp-client or --http-proxy or --socks-proxy is used)."),
("--nobind     ", "Do not bind to local address and port."),
("--dev tunX|tapX ", "tun/tap device (X can be omitted for dynamic device."),
("--dev-type dt", "Which device type are we using? (dt = tun or tap) Use this option only if the tun/tap device used with --dev"
                   + "does not begin with 'tun' or 'tap'."),
("--dev-node node ", "Explicitly set the device node rather than using /dev/net/tun, /dev/tun, /dev/tap, etc."),
("--lladdr hw", "Set the link layer address of the tap device."),
("--topology t", "Set --dev tun topology 'net30', 'p2p', or 'subnet'."),
("--tun-ipv6 ", "Build tun link capable of forwarding IPv6 traffic."),
("--ifconfig l rn ", "TUN - configure device to use IP address l as a local endpoint and rn as a remote endpoint. "
                   + "l & rn should be swapped on the other peer. l & rn must be private addresses outside of the subnets used by either peer."
                   + "TAP configure device to use IP address l as a local-endpoint and rn as a subnet mask."),
("--ifconfig-ipv6 l r ", "configure device to use IPv6 address l as local endpoint (as a /64) and r as remote endpoint"),   
("--ifconfig-noexec ", "Don't actually execute ifconfig/netsh command, instead pass --ifconfig parms by environment to scripts."),
("--ifconfig-nowarn ", "Don't warn if the --ifconfig option on this side of the connection doesn't match the remote side."),  
("--route network [netmask] [gateway] [metric] ", "Add route to routing table after connection is established.  Multiple routes can be specified."
                                                + "netmask default - 255.255.255.255"
                                                + "gateway default - taken from --route-gateway or --ifconfig"
                                                + "Specify default by leaving blank or setting to 'nil'."),
("--route-ipv6 network/bits [gateway] [metric] ", "Add IPv6 route to routing table after connection is established.  Multiple routes can be specified."
                                                + "gateway default taken from --route-ipv6-gateway or --ifconfig"),
("--max-routes n ", " Specify the maximum number of routes that may be definedor pulled from a server."),
("--route-gateway gw|'dhcp' ", "Specify a default gateway for use with --route."),
("--route-metric m ", "Specify a default metric for use with --route."),
("--route-delay n [w] ", "Delay n seconds after connection initiation before adding routes (may be 0).  If not specified, routes will be added immediately after tun/tap open.  On Windows, wait up to w seconds for TUN/TAP adapter to come up."),
("--route-up cmd  ", "Run command cmd after routes are added."),
("--route-pre-down cmd ", "Run command cmd before routes are removed."),
("--route-noexec  ", "Don't add routes automatically.  Instead pass routes to --route-up script using environmental variables."),
("--route-nopull  ", "When used with --client or --pull, accept options pushed by server EXCEPT for routes and dhcp options."),
("--allow-pull-fqdn ", "Allow client to pull DNS names from server for --ifconfig, --route, and --route-gateway."),
("--redirect-gateway [flags]", "Automatically execute routing commands to redirect all outgoing IP traffic through"
                             + "the VPN.  Add 'local' flag if both OpenVPN servers are directly connected via a common subnet, such as with WiFi."
                             + "Add 'def1' flag to set default route using using 0.0.0.0/1 and 128.0.0.0/1 rather than 0.0.0.0/0.  Add 'bypass-dhcp'" 
                             + "flag to add a direct route to DHCP server, bypassing tunnel. Add 'bypass-dns' flag to similarly bypass tunnel for DNS."),
("--redirect-private [flags]", "Like --redirect-gateway, but omit actually changing the default gateway.  Useful when pushing private subnets."),
("--client-nat snat|dnat network netmask alias ", "on client add 1-to-1 NAT rule."),
("--push-peer-info ", "(client only) push client info to server."),
("--setenv name value ", "Set a custom environmental variable to pass to script."),
("--setenv FORWARD_COMPATIBLE 1 ", "Relax config file syntax checking to allow directives for future OpenVPN versions to be ignored."),
("--ignore-unkown-option opt1 opt2 ...", "Relax config file syntax. Allow these options to be ignored when unknown"),
("--script-security level", "Where level can be" 
                          + "0 -- strictly no calling of external programs"
                          + "1 -- (default) only call built-ins such as ifconfig"
                          + "2 -- allow calling of built-ins and scripts"
                          + "3 -- allow password to be passed to scripts via env"),
("--shaper n ", "Restrict output to peer to n bytes per second."),
("--keepalive n m ", "Helper option for setting timeouts in server mode. Send ping once every n seconds, restart if ping not received for m seconds."),
("--inactive n [bytes] ", "Exit after n seconds of activity on tun/tap device produces a combined in/out byte count < bytes."),
("--ping-exit n", "Exit if n seconds pass without reception of remote ping."),
("--ping-restart n", "Restart if n seconds pass without reception of remote ping."),
("--ping-timer-rem", "Run the --ping-exit/--ping-restart timer only if we have a remote address."),
("--ping n", "Ping remote once every n seconds over TCP/UDP port."),
("--fast-io  ", "(experimental) Optimize TUN/TAP/UDP writes."),
("--remap-usr1 s  ", "On SIGUSR1 signals, remap signal (s='SIGHUP' or 'SIGTERM')."),
("--persist-tun", "Keep tun/tap device open across SIGUSR1 or --ping-restart."),
("--persist-remote-ip ", "Keep remote IP address across SIGUSR1 or --ping-restart."),
("--persist-local-ip  ", "Keep local IP address across SIGUSR1 or --ping-restart."),
("--persist-key", "Don't re-read key files across SIGUSR1 or --ping-restart."),
("--passtos  ", "TOS passthrough (applies to IPv4 only)."),
("--tun-mtu n", "Take the tun/tap device MTU to be n and derive the TCP/UDP MTU from it (default=1500)."),
("--tun-mtu-extra n ", "Assume that tun/tap device might return as many as n bytes more than the tun-mtu size on read"
                     + "(default TUN=0 TAP=32)."),
("--link-mtu n", "Take the TCP/UDP device MTU to be n and derive the tun MTU from it."),
("--mtu-disc type ", "Should we do Path MTU discovery on TCP/UDP channel?"
                   + "'no'    -- Never send DF (Don't Fragment) frames"
                   + "'maybe' -- Use per-route hints"
                   + "'yes'   -- Always DF (Don't Fragment)"),
("--mtu-test ", "Empirically measure and report MTU."),
("--fragment max  ", "Enable internal datagram fragmentation so that no UDP datagrams are sent which are larger than max bytes. Adds 4 bytes of overhead per datagram."),
("--mssfix [n]", "Set upper bound on TCP MSS, default = tun-mtu size or --fragment max value, whichever is lower."),
("--sndbuf size", "Set the TCP/UDP send buffer size."),
("--rcvbuf size", "Set the TCP/UDP receive buffer size."),
("--txqueuelen n  ", "Set the tun/tap TX queue length to n (Linux only)."),
("--mlock", "Disable Paging -- ensures key material and tunnel data will never be written to disk."),
("--up cmd", "Run command cmd after successful tun device open."
           + "Execute as cmd tun/tap-dev tun-mtu link-mtu \ifconfig-local-ip ifconfig-remote-ip"
           + "(pre --user or --group UID/GID change)"),
("--up-delay ", "Delay tun/tap open and possible --up script execution until after TCP/UDP connection establishment with peer."),
("--down cmd ", "Run command cmd after tun device close. (post --user/--group UID/GID change and/or --chroot)(command parameters are same as --up option)"),
("--down-pre ", "Run --down command before TUN/TAP close."),
("--up-restart", "Run up/down commands for all restarts including those caused by --ping-restart or SIGUSR1"),
("--user user", "Set UID to user after initialization."),
("--group group", "Set GID to group after initialization."),
("--chroot dir", "Chroot to this directory after initialization."),
("--cd dir", "Change to this directory before initialization."),
("--daemon [name] ", "Become a daemon after initialization. The optional 'name' parameter will be passed as the program name to the system logger."),
("--syslog [name] ", "Output to syslog, but do not become a daemon. See --daemon above for a description of the 'name' parm."),
("--inetd [name] ['wait'|'nowait'] ", "Run as an inetd or xinetd server. See --daemon above for a description of the 'name' parm."),
("--log file ", "Output log to file which is created/truncated on open."),
("--log-append file ", "Append log to file, or create file if nonexistent."),
("--suppress-timestamps ", "Don't log timestamps to stdout/stderr."),
("--writepid file ", "Write main process ID to file."),
("--nice n", "Change process priority (>0 = lower, <0 = higher)."),
("--echo [parms ...] ", "Echo parameters to log output."),
("--verb n", "Set output verbosity to n (default=1), (Level 3 is recommended if you want a good summary of what's happening without being swamped by output)."
         + "0 -- no output except fatal errors"
         + "1 -- startup info + connection initiated messages non-fatal encryption & net errors"                 
         + "2,3 -- show TLS negotiations & route info"
         + "4 -- show parameters"
         + "5 -- show 'RrWw' chars on console for each packet sent and received from TCP/UDP (caps) or tun/tap (lc)"                 
         + "6 to 11 -- debug messages of increasing verbosity"),
("--mute n", "Log at most n consecutive messages in the same category."),
("--status file n ", "Write operational status to file every n seconds."),
("--status-version [n] ", "Choose the status file format version number. Currently, n can be 1, 2, or 3 (default=1)."),
("--disable-occ", "Disable options consistency check between peers."),
("--gremlin mask  ", "Special stress testing mode (for debugging only)."),
("--comp-lzo ", "Use fast LZO compression -- may add up to 1 byte per packet for uncompressible data."),
("--comp-noadapt  ", "Don't use adaptive compression when --comp-lzo is specified."),
("--management ip port [pass] ", "Enable a TCP server on ip. port to handle management functions. pass is a password file or 'stdin' to prompt from console."),
("--management-client ", "Management interface will connect as a TCP client to ip/port rather than listen as a TCP server."),    
("--management-query-passwords ", "Query management channel for private key and auth-user-pass passwords."),
("--management-query-proxy ", "Query management channel for proxy information."),
("--management-query-remote ", "Query management channel for --remote directive."),
("--management-hold ", "Start OpenVPN in a hibernating state, until a client of the management interface explicitly starts it."),  
("--management-signal ", "Issue SIGUSR1 when management disconnect event occurs."),
("--management-forget-disconnect ", "Forget passwords when management disconnect event occurs."),               
("--management-up-down ", "Report tunnel up/down events to management interface."),
("--management-log-cache n ", "Cache n lines of log file history for usage by the management channel."),
("--management-client-auth ", "gives management interface client the responsibility to authenticate clients after their client certificate has been verified."),
("--management-client-pf ", "management interface clients must specify a packet filter file for each connecting client."),      
("--plugin m [str]", "Load plug-in module m passing str as an argument to its initialization function."),
# Multi-Client Server options (when --mode server is used)
("--server network netmask ", "Helper option to easily configure server mode."),
("--server-ipv6 network/bits ", "Configure IPv6 server mode."),
("--server-bridge [IP netmask pool-start-IP pool-end-IP] ", "Helper option to easily configure ethernet bridging server mode."),  
("--push 'option'", "Push a config file option back to the peer for remote execution.  Peer must specify --pull in its config file."),
("--push-reset", "Don't inherit global push list for specific client instance."),
("--ifconfig-pool start-IP end-IP [netmask] ", "Set aside a pool of subnets to be dynamically allocated to connecting clients."),
("--ifconfig-pool-linear ", "Use individual addresses rather than /30 subnets in tun mode.  Not compatible with Windows clients."),
("--ifconfig-pool-persist file [seconds] ", "Persist/unpersist ifconfig-pool data to file, at seconds intervals (default=600). If seconds=0, file will be treated as read-only."),
("--ifconfig-ipv6-pool base-IP/bits ", "set aside an IPv6 network block to be dynamically allocated to connecting clients."),
("--ifconfig-push local remote-netmask ", "Push an ifconfig option to remote, overrides --ifconfig-pool dynamic allocation. Only valid in a client-specific config file."),
("--ifconfig-ipv6-push local/bits remote ", "Push an ifconfig-ipv6 option to remote, overrides --ifconfig-ipv6-pool allocation. Only valid in a client-specific config file."),
("--iroute network [netmask] ", "Route subnet to client."),
("--iroute-ipv6 network/bits ", "Route IPv6 subnet to client. Sets up internal routes only. Only valid in a client-specific config file."),
("--disable  ", "Client is disabled. Only valid in a client-specific config file."),
("--client-cert-not-required ", "Don't require client certificate, client will authenticate using username/password."),
("--username-as-common-name  ", "For auth-user-pass authentication, use the authenticated username as the common name, rather than the common name from the client cert."),
("--auth-user-pass-verify cmd method", "Query client for username/password and run command cmd to verify.  If method='via-env', pass user/pass via environment, if method='via-file', pass user/pass via temporary file."),
("--opt-verify", "Clients that connect with options that are incompatible with those of the server will be disconnected."),
("--auth-user-pass-optional ", "Allow connections by clients that don't specify a username/password."),
("--no-name-remapping ", "Allow Common Name and X509 Subject to include any printable character."),   
("--client-to-client ", "Internally route client-to-client traffic."),
("--duplicate-cn  ", "Allow multiple clients with the same common name to concurrently connect."),
("--client-connect cmd ", "Run command cmd on client connection."),
("--client-disconnect cmd ", "Run command cmd on client disconnection."),
("--client-config-dir dir ", "Directory for custom client config files."),
("--ccd-exclusive ", "Refuse connection unless custom client config is found."),
("--tmp-dir dir", "Temporary directory, used for --client-connect return file and plugin communication."),
("--hash-size r v ", "Set the size of the real address hash table to r and the virtual address table to v."),
("--bcast-buffers n ", "Allocate n broadcast buffers."),
("--tcp-queue-limit n ", "Maximum number of queued TCP output packets."),
("--tcp-nodelay", "Macro that sets TCP_NODELAY socket flag on the server as well as pushes it to connecting clientons."),
("--learn-address cmd ", "Run command cmd to validate client virtual addresses."),
("--connect-freq n s ", "Allow a maximum of n new connections per s seconds."),
("--max-clients n ", "Allow a maximum of n simultaneously connected clients."),
("--max-routes-per-client n ", "Allow a maximum of n internal routes per client."),
("--stale-routes-check n [t] ", "Remove routes with a last activity timestamp older than n seconds. Run this check every t seconds (defaults to n)."),
# Client options (when connecting to a multi-client server)
("--client", "Helper option to easily configure client mode."),
("--auth-user-pass [up] ", "Authenticate with server using username/password. up is a file containing the username on the first line, and a password on the second. If either the password or both"
                         + "the username and the password are omitted OpenVPN will prompt for them from console."),
("--pull  ", "Accept certain config file options from the peer as if they were part of the local config file. Must be specified when connecting to a '--mode server' remote host."),
("--auth-retry t  ", "How to handle auth failures.  Set t to none (default), interact, or nointeract."),
("--static-challenge t e ", "Enable static challenge/response protocol using challenge text t, with e indicating echo flag (0|1)"),
("--server-poll-timeout n ", "when polling possible remote servers to connect to in a round-robin fashion, spend no more than n seconds waiting for a response before trying the next server."),
("--explicit-exit-notify [n] ", "On exit/restart, send exit signal to server/remote. n = # of retries, default=1."),
# ("Data Channel Encryption Options (must be compatible between peers)", "
# ("(These options are meaningful for both Static Key & TLS-mode)
("--secret f [d]  ", "Enable Static Key encryption mode (non-TLS). Use shared secret file f, generate with --genkey. The optional d parameter controls key directionality."
                   + "If d is specified, use separate keys for each direction, set d=0 on one side of the connection, and d=1 on the other side."),
("--auth alg ", "Authenticate packets with HMAC using message (usually adds 16 or 20 bytes per packet) Set alg=none to disable authentication."),
("--cipher alg", "Encrypt packets with cipher algorithm alg (default=BF-CBC). Set alg=none to disable encryption."),
("--prng alg [nsl] ", "For PRNG, use digest algorithm alg, and nonce_secret_len=nsl.  Set alg=none to disable PRNG."),
("--keysize n", "Size of cipher key in bits (optional). If unspecified, defaults to cipher-specific default."),
("--engine [name] ", "Enable OpenSSL hardware crypto engine functionality."),
("--no-replay", "Disable replay protection."),
("--mute-replay-warnings ", "Silence the output of replay warnings to log file."),
("--replay-window n [t]  ", "Use a replay protection sliding window of size n and a time window of t seconds. Default n=64 t=15"),
("--no-iv", "Disable cipher IV -- only allowed with CBC mode ciphers."),
("--replay-persist file ", "Persist replay-protection state across sessions using file."),
("--test-crypto", "Run a self-test of crypto features enabled."),
# For debugging only.
# TLS Key Negotiation Options
# These options are meaningful only for TLS-mode)
("--tls-server", "Enable TLS and assume server role during TLS handshake."),
("--tls-client", "Enable TLS and assume client role during TLS handshake."),
("--key-method m  ", "Data channel key exchange method.  m should be a method number, such as 1 (default), 2, etc."),
("--ca file  ", "Certificate authority file in .pem format containing root certificate."),
("--capath dir", "A directory of trusted certificates (CAs and CRLs)."),
("--dh file  ", "File containing Diffie Hellman parameters in .pem format (for --tls-server only). Use 'openssl dhparam -out dh1024.pem 1024' to generate."),
("--cert file", "Local certificate in .pem format -- must be signed by a Certificate Authority in --ca file."),
("--extra-certs file ", "one or more PEM certs that complete the cert chain."),
("--key file ", "Local private key in .pem format."),
("--tls-version-min <version> ['or-highest'] ", "sets the minimum TLS version we will accept from the peer.  If version is unrecognized and 'or-highest' is specified, require max TLS version supported by SSL implementation."),
("--tls-version-max <version> ", "sets the maximum TLS version we will use."),
("--pkcs12 file", "PKCS#12 file containing local private key, local certificate and optionally the root CA certificate."),
("--verify-hash", "Specify SHA1 fingerprint for level-1 cert."),
("--cryptoapicert select-string ", "Load the certificate and private key from the Windows Certificate System Store."),
("--tls-cipher l  ", "A list l of allowable TLS ciphers separated by (optional)."),
("  ", "Use --show-tls to see a list of supported TLS ciphers."),
("--tls-timeout n ", "Packet retransmit timeout on TLS control channel if no ACK from remote within n seconds (default=2)."),
("--reneg-bytes n ", "Renegotiate data chan. key after n bytes sent and recvd."),
("--reneg-pkts n  ", "Renegotiate data chan. key after n packets sent and recvd."),
("--reneg-sec n", "Renegotiate data chan. key after n seconds (default=3600)."),
("--hand-window n ", "Data channel key exchange must finalize within n seconds of handshake initiation by any peer (default=60)."),
("--tran-window n ", "Transition window -- old key can live this many seconds after new key renegotiation begins (default=3600)."),
("--single-session", "Allow only one session (reset state on restart)."),
("--tls-exit ", "Exit on TLS negotiation failure."),
("--tls-auth f [d]", "Add an additional layer of authentication on top of the TLS control channel to protect against DoS attacks. f (required) is a shared-secret passphrase file. The optional d parameter controls key directionality, see --secret option for more info."),
("--askpass [file]", "Get PEM password from controlling tty before we daemonize."),
("--auth-nocache  ", "Don't cache --askpass or --auth-user-pass passwords."),
("--crl-verify crl ['dir']", "Check peer certificate against a CRL."),
("--tls-verify cmd", "Run command cmd to verify the X509 name of a pending TLS connection that has otherwise passed all other tests of certification.  cmd should return 0 to allow TLS handshake to proceed, or 1 to fail.  (cmd is executed as 'cmd certificate_depth subject')"),
("--tls-export-cert [directory] ", "Get peer cert in PEM format and store it in an openvpn temporary file in [directory]. Peer cert is stored before tls-verify script execution and deleted after."),
("--verify-x509-name name", "Accept connections only from a host with X509 subject DN name. The remote host must also pass all other tests of verification."),
("--ns-cert-type t", "Require that peer certificate was signed with an explicit nsCertType designation t = 'client' | 'server'."),
("--x509-track x  ", "Save peer X509 attribute x in environment for use by plugins and management interface."),
("--remote-cert-ku v ... ", "Require that the peer certificate was signed with explicit key usage, you can specify more than one value. value should be given in hex format."),
("--remote-cert-eku oid ", "Require that the peer certificate was signed with explicit extended key usage. Extended key usage can be encoded as an object identifier or OpenSSL string representation."),
("--remote-cert-tls t", "Require that peer certificate was signed with explicit key usage and extended key usage based on RFC3280 TLS rules. t = 'client' | 'server'."),
# PKCS#11 Options
("--pkcs11-providers provider ... ", "PKCS#11 provider to load."),
("--pkcs11-protected-authentication [0|1] ... ", "Use PKCS#11 protected authentication path. Set for each provider."),
("--pkcs11-private-mode hex ...", "PKCS#11 private key mode mask."
            + "0 - Try  to determind automatically (default)."
            + "1 - Use Sign."
            + "3 - Use SignRecover."
            + "4 - Use Decrypt."
            + "5 - Use Unwrap."),
("--pkcs11-cert-private [0|1] ... ", "Set if login should be performed before certificate can be accessed. Set for each provider."),                
("--pkcs11-pin-cache seconds ", "Number of seconds to cache PIN. The default is -1 cache until token is removed."),                
("--pkcs11-id-management ", "Acquire identity from management interface."),
("--pkcs11-id serialized-id 'id'  ", "Identity to use, get using standalone --show-pkcs11-ids"),
# SSL Library information
("--show-ciphers  ", "Show cipher algorithms to use with --cipher option."),
("--show-digests  ", "Show message digest algorithms to use with --auth option."),
("--show-engines  ", "Show hardware crypto accelerator engines (if available)."),
("--show-tls ", "Show all TLS ciphers (TLS used only as a control channel)."),
# Windows Specific
("--win-sys path", "Pathname of Windows system directory. Default is the pathname from SystemRoot environment variable."),
("--ip-win32 method ", "When using --ifconfig on Windows, set TAP-Windows adapter IP address using method = manual, netsh, ipapi,"                  
                     + "dynamic, or adaptive (default = adaptive). Dynamic method allows two optional parameters"                      
                     + "offset DHCP server address offset (> -256 and < 256)."
                     + " If 0, use network address, if >0, take nth"
                     + " address forward from network address, if <0"
                     + " take nth address backward from broadcast address."                     
                     + " Default is 0. Lease time in seconds. Default is one year."),
("--route-method", "Which method to use for adding routes on Windows?"
                 + "adaptive (default) -- Try ipapi then fall back to exe."
                 + "ipapi -- Use IP helper API."
                 + "exe -- Call the route.exe shell command."),
("--dhcp-option type [parm] ", "Set extended TAP-Windows properties, must be used with --ip-win32 dynamic.  For options"                              
                             + "which allow multiple addresses, --dhcp-option must be repeated."
                             + "DOMAIN name - Set DNS suffix"
                             + "DNS addr - Set domain name server address(es)"
                             + "NTP - Set NTP server address(es)"
                             + "NBDD - Set NBDD server address(es)"
                             + "WINS addr - Set WINS server address(es)"
                             + "NBT type - Set NetBIOS over TCP/IP Node type 1 = B, 2 = P, 4 = M, 8 = H"                                            
                             + "NBS id - Set NetBIOS scope ID"
                             + "DISABLE-NBT - Disable Netbios-over-TCP/IP."),
("--dhcp-renew  ", "Ask Windows to renew the TAP adapter lease on startup."),
("--dhcp-pre-release ", "Ask Windows to release the previous TAP adapter lease on startup."),
("--dhcp-release", "Ask Windows to release the TAP adapter lease on shutdown."),
("--register-dns  ", "Run net stop dnscache, net start dnscache, ipconfig /flushdns and ipconfig /registerdns on connection initiation."),
("--tap-sleep n", "Sleep for n seconds after TAP adapter open before attempting to set adapter properties."),
("--pause-exit", "When run from a console window, pause before exiting."),
("--service ex [0|1]", "For use when OpenVPN is being instantiated by a service, and should not be used directly by end-users."     
                     + "ex is the name of an event object which, when signaled, will cause OpenVPN to exit.  A second "             
                     + "optional parameter controls the initial state of ex."),
("--show-net-up", "Show OpenVPN's view of routing table and net adapter list after TAP adapter is up and routes have been added."),
("--block-outside-dns", "Block DNS on other network adapters to prevent DNS leaks"),
# Windows Standalone Options
("--show-adapters ", "Show all TAP-Windows adapters."),
("--show-net ", "Show OpenVPN's view of routing table and net adapter list."),
("--show-valid-subnets ", "Show valid subnets for --dev tun emulation."),
("--allow-nonadmin [TAP-adapter] ", "Allow OpenVPN running without admin privileges to access TAP adapter."),              
# Generate a random key (only for non-TLS static key encryption mode)
("--genkey", "Generate a random key to be used as a shared secret, for use with the --secret option."),
("--secret file", "Write key to file."),
# PKCS#11 standalone options"
("--show-pkcs11-ids [provider] [cert_private] ", "Show PKCS#11 available ids. --verb option can be added *BEFORE* this."),                        
# General Standalone Options
("--show-gateway ", "Show info about default gateway.")]

                        
class CommandOutput(wx.TextCtrl):
    """ multiline text control for displaying output """
    
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, 
                             parent,
                             style=wx.TE_MULTILINE)
                             
        self.SetFont = CMDOUTPUTFONT
        self.SetBackgroundColour(CMDOUTPUTBGCOLOUR)
        self.SetForegroundColour(CMDOUTPUTFGCOLOUR)
        
        #catch important messages or errors   
        self.important = ["Enter Auth Username:Options error: --auth-user-pass fails with",
                          "Enter Auth Username:"]
        self.messages = ["Initialization Sequence Completed",
                         "Successful ARP Flush on interface",]
        self.errors = ["frag ttl expired" ] #express vpn : unstable connection? change protocol?
        self.ignore = ["Options error: Please correct these errors."]                
            
        
class FlagsList(wx.ListCtrl, ListCtrlAutoWidthMixin):
    """ populates list with openvpn commandline arguments """
    
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, 
                             parent,
                             style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        
        ListCtrlAutoWidthMixin.__init__(self)
        
        self.AppendColumn("cmd")
        self.AppendColumn("about")
        
        options = CMDFLAGS
        for op in options:   
            print(op)
            self.Append(op)

class Flags(BasePanel):
    """ navigate different """
    
    def __init__(self, parent):
        BasePanel.__init__(self, 
                           parent)
                           
        sizer = wx.BoxSizer(wx.HORIZONTAL)                    
        splitter = wx.SplitterWindow(self)
        self.output = CommandOutput(splitter)
        self.list = FlagsList(splitter)
        
        splitter.SplitHorizontally(self.output, self.list)
        splitter.SetSashGravity(0.5)
        sizer.Add(splitter, 1, wx.ALL|wx.EXPAND)
        self.SetSizer(sizer)
        
        #Bindings
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnListItemActivated)
        
    def OnListItemActivated(self, event):
        e = event.GetIndex()
        
        param = self.list.GetItemText(e)     
        self.DoRunCmd(param)
        
    def DoRunCmd(self, param):        
        # param = msg.data 
        if param == "--config":
            os.chdir("c:/")
            print(os.getcwd())
            # print(os.system("dir"))  
            admin.run_as_admin([""])
            time.sleep(2)
            p = subprocess.Popen("openvpn.exe --config uk.ovpn --daemon", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # SubCall("openvpn.exe --config uk.ovpn")
        else:                    
            p = subprocess.Popen("openvpn.exe " + param, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            # pub.sendMessage("PubAppendText", out)
            self.output.AppendText("#")
            self.output.AppendText("-----"*5)
            self.output.AppendText("\n")
            self.output.AppendText(out)
            self.output.AppendText("-----"*5)
            self.output.AppendText("#")
            self.output.AppendText("\n")
            
    def AppendText(self, msg):
        try:
            text = msg.data.decode("utf8")
        except:
            text = msg.data
        
        hasIgnore = [ig for ig in self.ignore if ig in text]
        if hasIgnore:
            item = self.Append(["", "", text])
            self.SetItemTextColour(item, "yellow")
            return
            
        #try to catch important messages early
        hasImportant = [imp for imp in self.important if imp in text]
        if hasImportant:
            item = self.Append(["", "!", text])
            self.SetItemTextColour(item, "red")
            return
            
        #here we split the date from the log message
        text_list = text.split(" ")
        for n, s in enumerate(text_list):
            try:
                int(text_list[n][-1])
                try:
                    int(text_list[n+1][0])
                except:
                    text_str = " ".join(text_list[n+1:])
                    date = " ".join(text_list[:n+1])
                    break
            except:        
                continue
        
        
        try: 
            hasMessage = [message for message in self.messages if message in text_str]
            hasError = [err for err in self.errors if err in text_str]
            
            if hasMessage:
                item = self.Append([date, ":)", text_str])
                self.SetItemTextColour(self.GetItemCount()-1, OUTPUTMESSAGEFGCOLOUR)
            elif hasMessage:
                item = self.Append([date, "Error", text_str])
                self.SetItemTextColour(item, OUTPUTERRORFGCOLOUR)
                self.Focus() #focus on error message
            else:
                item = self.Append([date, "", text_str])
                self.SetItemTextColour(item, OUTPUTFGCOLOUR)
            print(hasMessage)
            self.EnsureVisible(self.GetItemCount()-1) #auto scroll
        except:
            print (text)
        
        self.SetForegroundColour(OUTPUTFGCOLOUR)
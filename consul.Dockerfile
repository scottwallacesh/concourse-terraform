ARG PARENT_IMAGE=snapkitchen/concourse-consul:latest
FROM alpine:3.8 as build
# based on the official hashicorp consul image
# at https://raw.githubusercontent.com/hashicorp/docker-consul/master/0.X/Dockerfile

ARG CONSUL_VERSION=0.0.0

COPY hashicorp.asc .

RUN apk add --no-cache --update \
      curl \
      gnupg \
      openssh \
      && \
    curl https://releases.hashicorp.com/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_SHA256SUMS.sig > consul_${CONSUL_VERSION}_SHA256SUMS.sig && \
    curl https://releases.hashicorp.com/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_SHA256SUMS > consul_${CONSUL_VERSION}_SHA256SUMS && \
    gpg --import hashicorp.asc && \
    gpg --verify consul_${CONSUL_VERSION}_SHA256SUMS.sig consul_${CONSUL_VERSION}_SHA256SUMS && \
    curl https://releases.hashicorp.com/consul/${CONSUL_VERSION}/consul_${CONSUL_VERSION}_linux_amd64.zip > consul_${CONSUL_VERSION}_linux_amd64.zip && \
    cat consul_${CONSUL_VERSION}_SHA256SUMS | grep consul_${CONSUL_VERSION}_linux_amd64.zip | sha256sum -c && \
    unzip consul_${CONSUL_VERSION}_linux_amd64.zip -d /bin && \
    rm -f consul_${CONSUL_VERSION}_SHA256SUMS.sig \
      consul_${CONSUL_VERSION}_SHA256SUMS \
      consul_${CONSUL_VERSION}_linux_amd64.zip \
      hashicorp.asc

FROM $PARENT_IMAGE
# based on the official hashicorp consul image
# at https://raw.githubusercontent.com/hashicorp/docker-consul/master/0.X/Dockerfile

COPY --from=build /bin/consul /bin/consul

RUN consul version && \
    apk add --no-cache --update \
      dumb-init \
      iptables

# The /consul/data dir is used by Consul to store state. The agent will be started
# with /consul/config as the configuration directory so you can add additional
# config files in that location.
RUN mkdir -p /consul/data && \
    mkdir -p /consul/config

# set up nsswitch.conf for Go's "netgo" implementation which is used by Consul,
# otherwise DNS supercedes the container's hosts file, which we don't want.
RUN test -e /etc/nsswitch.conf || echo 'hosts: files dns' > /etc/nsswitch.conf

# Expose the consul data directory as a volume since there's mutable state in there.
VOLUME /consul/data

# Server RPC is used for communication between Consul clients and servers for internal
# request forwarding.
EXPOSE 8300

# Serf LAN and WAN (WAN is used only by Consul servers) are used for gossip between
# Consul agents. LAN is within the datacenter and WAN is between just the Consul
# servers in all datacenters.
EXPOSE 8301 8301/udp 8302 8302/udp

# HTTP and DNS (both TCP and UDP) are the primary interfaces that applications
# use to interact with Consul.
EXPOSE 8500 8600 8600/udp

# We diverge here to configure the entry point
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["/bin/sh"]

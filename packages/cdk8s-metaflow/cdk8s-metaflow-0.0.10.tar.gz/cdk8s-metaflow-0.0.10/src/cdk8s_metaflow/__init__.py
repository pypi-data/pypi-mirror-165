'''
# cdk8s-metaflow

Collection of cdk8s constructs for deploying [Metaflow](https://metaflow.org) on Kubernetes.

### Imports

```shell
cdk8s import k8s@1.22.0 -l typescript -o src/imports
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add argo https://charts.bitnami.com/bitnami
helm repo add autoscaler https://kubernetes.github.io/autoscaler
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import cdk8s
import cdk8s_plus_21
import constructs


@jsii.data_type(
    jsii_type="cdk8s-metaflow.DatabaseAuthOptions",
    jsii_struct_bases=[],
    name_mapping={
        "database": "database",
        "enable_postgres_user": "enablePostgresUser",
        "password": "password",
        "postgres_password": "postgresPassword",
        "replication_password": "replicationPassword",
        "replication_username": "replicationUsername",
        "username": "username",
    },
)
class DatabaseAuthOptions:
    def __init__(
        self,
        *,
        database: typing.Optional[builtins.str] = None,
        enable_postgres_user: typing.Optional[builtins.bool] = None,
        password: typing.Optional[builtins.str] = None,
        postgres_password: typing.Optional[builtins.str] = None,
        replication_password: typing.Optional[builtins.str] = None,
        replication_username: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database: 
        :param enable_postgres_user: 
        :param password: 
        :param postgres_password: 
        :param replication_password: 
        :param replication_username: 
        :param username: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DatabaseAuthOptions.__init__)
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument enable_postgres_user", value=enable_postgres_user, expected_type=type_hints["enable_postgres_user"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument postgres_password", value=postgres_password, expected_type=type_hints["postgres_password"])
            check_type(argname="argument replication_password", value=replication_password, expected_type=type_hints["replication_password"])
            check_type(argname="argument replication_username", value=replication_username, expected_type=type_hints["replication_username"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {}
        if database is not None:
            self._values["database"] = database
        if enable_postgres_user is not None:
            self._values["enable_postgres_user"] = enable_postgres_user
        if password is not None:
            self._values["password"] = password
        if postgres_password is not None:
            self._values["postgres_password"] = postgres_password
        if replication_password is not None:
            self._values["replication_password"] = replication_password
        if replication_username is not None:
            self._values["replication_username"] = replication_username
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def database(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("database")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_postgres_user(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enable_postgres_user")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def postgres_password(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("postgres_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_password(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("replication_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def replication_username(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("replication_username")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseAuthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s-metaflow.DatabaseMetricsOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class DatabaseMetricsOptions:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param enabled: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DatabaseMetricsOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseMetricsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s-metaflow.DatabaseReplicationOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "read_replicas": "readReplicas"},
)
class DatabaseReplicationOptions:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        read_replicas: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: 
        :param read_replicas: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DatabaseReplicationOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument read_replicas", value=read_replicas, expected_type=type_hints["read_replicas"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if read_replicas is not None:
            self._values["read_replicas"] = read_replicas

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_replicas(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("read_replicas")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseReplicationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s-metaflow.DatabaseResourceRequestOptions",
    jsii_struct_bases=[],
    name_mapping={"cpu": "cpu", "memory": "memory"},
)
class DatabaseResourceRequestOptions:
    def __init__(
        self,
        *,
        cpu: typing.Optional[builtins.str] = None,
        memory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cpu: 
        :param memory: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DatabaseResourceRequestOptions.__init__)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
        self._values: typing.Dict[str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if memory is not None:
            self._values["memory"] = memory

    @builtins.property
    def cpu(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseResourceRequestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s-metaflow.DatabaseResourcesOptions",
    jsii_struct_bases=[],
    name_mapping={"requests": "requests"},
)
class DatabaseResourcesOptions:
    def __init__(
        self,
        *,
        requests: typing.Optional[typing.Union[DatabaseResourceRequestOptions, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param requests: 

        :stability: experimental
        '''
        if isinstance(requests, dict):
            requests = DatabaseResourceRequestOptions(**requests)
        if __debug__:
            type_hints = typing.get_type_hints(DatabaseResourcesOptions.__init__)
            check_type(argname="argument requests", value=requests, expected_type=type_hints["requests"])
        self._values: typing.Dict[str, typing.Any] = {}
        if requests is not None:
            self._values["requests"] = requests

    @builtins.property
    def requests(self) -> typing.Optional[DatabaseResourceRequestOptions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("requests")
        return typing.cast(typing.Optional[DatabaseResourceRequestOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseResourcesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s-metaflow.DatabaseVolumePermissionsOptions",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class DatabaseVolumePermissionsOptions:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param enabled: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(DatabaseVolumePermissionsOptions.__init__)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseVolumePermissionsOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s-metaflow.HelmPostgresAddonProps",
    jsii_struct_bases=[],
    name_mapping={
        "chart_version": "chartVersion",
        "namespace_name": "namespaceName",
        "chart_values": "chartValues",
    },
)
class HelmPostgresAddonProps:
    def __init__(
        self,
        *,
        chart_version: builtins.str,
        namespace_name: builtins.str,
        chart_values: typing.Optional[typing.Union["MetadataDatabaseOptions", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param chart_version: 
        :param namespace_name: 
        :param chart_values: 

        :stability: experimental
        '''
        if isinstance(chart_values, dict):
            chart_values = MetadataDatabaseOptions(**chart_values)
        if __debug__:
            type_hints = typing.get_type_hints(HelmPostgresAddonProps.__init__)
            check_type(argname="argument chart_version", value=chart_version, expected_type=type_hints["chart_version"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
            check_type(argname="argument chart_values", value=chart_values, expected_type=type_hints["chart_values"])
        self._values: typing.Dict[str, typing.Any] = {
            "chart_version": chart_version,
            "namespace_name": namespace_name,
        }
        if chart_values is not None:
            self._values["chart_values"] = chart_values

    @builtins.property
    def chart_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("chart_version")
        assert result is not None, "Required property 'chart_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def chart_values(self) -> typing.Optional["MetadataDatabaseOptions"]:
        '''
        :stability: experimental
        '''
        result = self._values.get("chart_values")
        return typing.cast(typing.Optional["MetadataDatabaseOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmPostgresAddonProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk8s-metaflow.IAddon")
class IAddon(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="install")
    def install(self, scope: constructs.Construct) -> constructs.Construct:
        '''
        :param scope: -

        :stability: experimental
        '''
        ...


class _IAddonProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk8s-metaflow.IAddon"

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @jsii.member(jsii_name="install")
    def install(self, scope: constructs.Construct) -> constructs.Construct:
        '''
        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(IAddon.install)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(constructs.Construct, jsii.invoke(self, "install", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAddon).__jsii_proxy_class__ = lambda : _IAddonProxy


@jsii.implements(IAddon)
class LocalPostgresAddon(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s-metaflow.LocalPostgresAddon",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        endpoint_ip: builtins.str,
        namespace_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_ip: 
        :param namespace_name: 

        :stability: experimental
        '''
        props = LocalPostgresAddonProps(
            endpoint_ip=endpoint_ip, namespace_name=namespace_name
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="install")
    def install(self, scope: constructs.Construct) -> constructs.Construct:
        '''
        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LocalPostgresAddon.install)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(constructs.Construct, jsii.invoke(self, "install", [scope]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NAME")
    def NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "NAME"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="cdk8s-metaflow.LocalPostgresAddonProps",
    jsii_struct_bases=[],
    name_mapping={"endpoint_ip": "endpointIp", "namespace_name": "namespaceName"},
)
class LocalPostgresAddonProps:
    def __init__(
        self,
        *,
        endpoint_ip: builtins.str,
        namespace_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint_ip: 
        :param namespace_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(LocalPostgresAddonProps.__init__)
            check_type(argname="argument endpoint_ip", value=endpoint_ip, expected_type=type_hints["endpoint_ip"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "endpoint_ip": endpoint_ip,
        }
        if namespace_name is not None:
            self._values["namespace_name"] = namespace_name

    @builtins.property
    def endpoint_ip(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("endpoint_ip")
        assert result is not None, "Required property 'endpoint_ip' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_name(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("namespace_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocalPostgresAddonProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s-metaflow.MetadataDatabaseOptions",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "auth": "auth",
        "metrics": "metrics",
        "replication": "replication",
        "resources": "resources",
        "volume_permissions": "volumePermissions",
    },
)
class MetadataDatabaseOptions:
    def __init__(
        self,
        *,
        architecture: typing.Optional[builtins.str] = None,
        auth: typing.Optional[typing.Union[DatabaseAuthOptions, typing.Dict[str, typing.Any]]] = None,
        metrics: typing.Optional[typing.Union[DatabaseMetricsOptions, typing.Dict[str, typing.Any]]] = None,
        replication: typing.Optional[typing.Union[DatabaseReplicationOptions, typing.Dict[str, typing.Any]]] = None,
        resources: typing.Optional[typing.Union[DatabaseResourcesOptions, typing.Dict[str, typing.Any]]] = None,
        volume_permissions: typing.Optional[typing.Union[DatabaseVolumePermissionsOptions, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param architecture: 
        :param auth: 
        :param metrics: 
        :param replication: 
        :param resources: 
        :param volume_permissions: 

        :stability: experimental
        '''
        if isinstance(auth, dict):
            auth = DatabaseAuthOptions(**auth)
        if isinstance(metrics, dict):
            metrics = DatabaseMetricsOptions(**metrics)
        if isinstance(replication, dict):
            replication = DatabaseReplicationOptions(**replication)
        if isinstance(resources, dict):
            resources = DatabaseResourcesOptions(**resources)
        if isinstance(volume_permissions, dict):
            volume_permissions = DatabaseVolumePermissionsOptions(**volume_permissions)
        if __debug__:
            type_hints = typing.get_type_hints(MetadataDatabaseOptions.__init__)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument replication", value=replication, expected_type=type_hints["replication"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument volume_permissions", value=volume_permissions, expected_type=type_hints["volume_permissions"])
        self._values: typing.Dict[str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if auth is not None:
            self._values["auth"] = auth
        if metrics is not None:
            self._values["metrics"] = metrics
        if replication is not None:
            self._values["replication"] = replication
        if resources is not None:
            self._values["resources"] = resources
        if volume_permissions is not None:
            self._values["volume_permissions"] = volume_permissions

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth(self) -> typing.Optional[DatabaseAuthOptions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[DatabaseAuthOptions], result)

    @builtins.property
    def metrics(self) -> typing.Optional[DatabaseMetricsOptions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[DatabaseMetricsOptions], result)

    @builtins.property
    def replication(self) -> typing.Optional[DatabaseReplicationOptions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("replication")
        return typing.cast(typing.Optional[DatabaseReplicationOptions], result)

    @builtins.property
    def resources(self) -> typing.Optional[DatabaseResourcesOptions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[DatabaseResourcesOptions], result)

    @builtins.property
    def volume_permissions(self) -> typing.Optional[DatabaseVolumePermissionsOptions]:
        '''
        :stability: experimental
        '''
        result = self._values.get("volume_permissions")
        return typing.cast(typing.Optional[DatabaseVolumePermissionsOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetadataDatabaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk8s-metaflow.MetaflowChartProps",
    jsii_struct_bases=[cdk8s.ChartProps],
    name_mapping={
        "labels": "labels",
        "namespace": "namespace",
        "image": "image",
        "image_tag": "imageTag",
        "service_port": "servicePort",
        "env_vars": "envVars",
        "init_image": "initImage",
        "init_image_tag": "initImageTag",
        "service_account": "serviceAccount",
    },
)
class MetaflowChartProps(cdk8s.ChartProps):
    def __init__(
        self,
        *,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        image: builtins.str,
        image_tag: builtins.str,
        service_port: typing.Union[cdk8s_plus_21.ServicePort, typing.Dict[str, typing.Any]],
        env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        init_image: typing.Optional[builtins.str] = None,
        init_image_tag: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[cdk8s_plus_21.IServiceAccount] = None,
    ) -> None:
        '''
        :param labels: Labels to apply to all resources in this chart. Default: - no common labels
        :param namespace: The default namespace for all objects defined in this chart (directly or indirectly). This namespace will only apply to objects that don't have a ``namespace`` explicitly defined for them. Default: - no namespace is synthesized (usually this implies "default")
        :param image: 
        :param image_tag: 
        :param service_port: 
        :param env_vars: 
        :param init_image: 
        :param init_image_tag: 
        :param service_account: 

        :stability: experimental
        '''
        if isinstance(service_port, dict):
            service_port = ServicePort(**service_port)
        if __debug__:
            type_hints = typing.get_type_hints(MetaflowChartProps.__init__)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument service_port", value=service_port, expected_type=type_hints["service_port"])
            check_type(argname="argument env_vars", value=env_vars, expected_type=type_hints["env_vars"])
            check_type(argname="argument init_image", value=init_image, expected_type=type_hints["init_image"])
            check_type(argname="argument init_image_tag", value=init_image_tag, expected_type=type_hints["init_image_tag"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
        self._values: typing.Dict[str, typing.Any] = {
            "image": image,
            "image_tag": image_tag,
            "service_port": service_port,
        }
        if labels is not None:
            self._values["labels"] = labels
        if namespace is not None:
            self._values["namespace"] = namespace
        if env_vars is not None:
            self._values["env_vars"] = env_vars
        if init_image is not None:
            self._values["init_image"] = init_image
        if init_image_tag is not None:
            self._values["init_image_tag"] = init_image_tag
        if service_account is not None:
            self._values["service_account"] = service_account

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Labels to apply to all resources in this chart.

        :default: - no common labels
        '''
        result = self._values.get("labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''The default namespace for all objects defined in this chart (directly or indirectly).

        This namespace will only apply to objects that don't have a
        ``namespace`` explicitly defined for them.

        :default: - no namespace is synthesized (usually this implies "default")
        '''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_tag(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_port(self) -> cdk8s_plus_21.ServicePort:
        '''
        :stability: experimental
        '''
        result = self._values.get("service_port")
        assert result is not None, "Required property 'service_port' is missing"
        return typing.cast(cdk8s_plus_21.ServicePort, result)

    @builtins.property
    def env_vars(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("env_vars")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def init_image(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("init_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def init_image_tag(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("init_image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_account(self) -> typing.Optional[cdk8s_plus_21.IServiceAccount]:
        '''
        :stability: experimental
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[cdk8s_plus_21.IServiceAccount], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetaflowChartProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MetaflowService(
    cdk8s.Chart,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s-metaflow.MetaflowService",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        name: builtins.str,
        *,
        image: builtins.str,
        image_tag: builtins.str,
        service_port: typing.Union[cdk8s_plus_21.ServicePort, typing.Dict[str, typing.Any]],
        env_vars: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        init_image: typing.Optional[builtins.str] = None,
        init_image_tag: typing.Optional[builtins.str] = None,
        service_account: typing.Optional[cdk8s_plus_21.IServiceAccount] = None,
        labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param image: 
        :param image_tag: 
        :param service_port: 
        :param env_vars: 
        :param init_image: 
        :param init_image_tag: 
        :param service_account: 
        :param labels: Labels to apply to all resources in this chart. Default: - no common labels
        :param namespace: The default namespace for all objects defined in this chart (directly or indirectly). This namespace will only apply to objects that don't have a ``namespace`` explicitly defined for them. Default: - no namespace is synthesized (usually this implies "default")

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(MetaflowService.__init__)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = MetaflowChartProps(
            image=image,
            image_tag=image_tag,
            service_port=service_port,
            env_vars=env_vars,
            init_image=init_image,
            init_image_tag=init_image_tag,
            service_account=service_account,
            labels=labels,
            namespace=namespace,
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> typing.Optional[cdk8s_plus_21.IServiceAccount]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[cdk8s_plus_21.IServiceAccount], jsii.get(self, "serviceAccount"))


@jsii.implements(IAddon)
class HelmPostgresAddon(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk8s-metaflow.HelmPostgresAddon",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        *,
        chart_version: builtins.str,
        namespace_name: builtins.str,
        chart_values: typing.Optional[typing.Union[MetadataDatabaseOptions, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''
        :param chart_version: 
        :param namespace_name: 
        :param chart_values: 

        :stability: experimental
        '''
        props = HelmPostgresAddonProps(
            chart_version=chart_version,
            namespace_name=namespace_name,
            chart_values=chart_values,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="install")
    def install(self, scope: constructs.Construct) -> constructs.Construct:
        '''
        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(HelmPostgresAddon.install)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(constructs.Construct, jsii.invoke(self, "install", [scope]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NAME")
    def NAME(cls) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "NAME"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


__all__ = [
    "DatabaseAuthOptions",
    "DatabaseMetricsOptions",
    "DatabaseReplicationOptions",
    "DatabaseResourceRequestOptions",
    "DatabaseResourcesOptions",
    "DatabaseVolumePermissionsOptions",
    "HelmPostgresAddon",
    "HelmPostgresAddonProps",
    "IAddon",
    "LocalPostgresAddon",
    "LocalPostgresAddonProps",
    "MetadataDatabaseOptions",
    "MetaflowChartProps",
    "MetaflowService",
]

publication.publish()

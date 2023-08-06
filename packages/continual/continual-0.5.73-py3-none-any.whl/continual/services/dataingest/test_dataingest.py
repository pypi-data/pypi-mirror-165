import os
import yaml
import time
import pytest
import shortuuid

from continual.rpc.management.v1 import management_types_pb2
from continual.rpc.dataingest.v1 import dataingest_pb2

from continual.python.sdk.features.featurestore import get_featurestore
from continual.services.dataingest.server import DataIngestService

TEST_CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".continual/testcfg.yaml")


@pytest.fixture(scope="session")
def postgres_mgmt():
    os.environ["CONFIG_ENV"] = "test"
    project_id = "testproject_" + shortuuid.uuid().lower()
    fstore = get_featurestore(projectid=project_id)
    fstore.cleanup()
    fstore.create_project_schema()
    fstore.load_data("gs://continual-dev/testing_data/train1.csv", project_id, "tweets")
    fstore.load_data(
        "gs://continual-dev/testing_data/username.csv", project_id, "twitter_user_raw"
    )
    fstore.load_data(
        "gs://continual-dev/testing_data/bank_train.csv", project_id, "bank_train"
    )

    fstore.load("./continual/services/dataingest/testdata/v2")

    mgmt = ManagementDummy(feature_store=fstore, project_id=project_id)
    print("Postgres featurestore ready")
    time.sleep(2)
    return mgmt


@pytest.fixture(scope="session")
def snowflake_mgmt():
    sf_datastore = get_snowflake_datastore()
    mgmt_snowflake = None
    if sf_datastore is None:
        return None

    project_id = "testproject_" + shortuuid.uuid().lower()
    if not sf_datastore.snowflake.db_schema:
        sf_datastore.snowflake.db_schema = project_id
    fstore = get_featurestore(sf_datastore, projectid=project_id)
    fstore.cleanup()
    fstore.create_project_schema()
    fstore.load_data(
        "gs://continual-dev/testing_data/train1.csv", project_id, "tweets_raw"
    )
    fstore.load_data(
        "gs://continual-dev/testing_data/username.csv", project_id, "twitter_user_raw"
    )
    fstore.load_data(
        "gs://continual-dev/testing_data/bank_train.csv", project_id, "bank_train"
    )
    fstore.load("./examples/twitter/v2")
    fstore.load("./examples/bank_marketing/v2")
    mgmt_snowflake = ManagementDummy(feature_store=fstore, project_id=project_id)

    print("Snowflake featurestore ready")
    return mgmt_snowflake


@pytest.fixture(scope="session")
def bigquery_mgmt():
    bq_datastore = get_bigquery_datastore()
    mgmt_bq = None
    if bq_datastore is None:
        return None

    project_id = "testproject_" + shortuuid.uuid().lower()
    fstore = get_featurestore(bq_datastore, projectid=project_id)
    fstore.cleanup()
    fstore.create_project_schema()
    fstore.load_data(
        "gs://continual-dev/testing_data/train1.csv", project_id, "tweets_raw"
    )
    fstore.load_data(
        "gs://continual-dev/testing_data/username.csv", project_id, "twitter_user_raw"
    )
    fstore.load_data(
        "gs://continual-dev/testing_data/bank_train.csv", project_id, "bank_train"
    )
    fstore.load("./examples/twitter/bigquery")
    fstore.load("./examples/bank_marketing/bigquery")
    mgmt_bq = ManagementDummy(feature_store=fstore, project_id=project_id)

    print("Snowflake featurestore ready")
    return mgmt_bq


@pytest.fixture
def mssql_mgmt():
    ms_datastore = get_mssql_datastore()
    mgmt_sqlserver = None
    if ms_datastore is None:
        return None

    project_id = "testproject_" + shortuuid.uuid().lower()
    fstore = get_featurestore(ms_datastore, projectid=project_id)
    fstore.cleanup()
    fstore.load("./examples/twitter/v2")
    mgmt_sqlserver = ManagementDummy(feature_store=fstore, project_id=project_id)
    print("Mssql featurestore ready")
    return mgmt_sqlserver


@pytest.fixture(scope="session")
def databricks_mgmt():
    print("Going to databricks management")
    db_datastore = get_databricks_datastore()
    if db_datastore is None:
        return None

    project_id = "testproject_" + shortuuid.uuid().lower()
    if not db_datastore.databricks.db_schema:
        db_datastore.databricks.db_schema = project_id
    fstore = get_featurestore(db_datastore, projectid=project_id)
    fstore.cleanup()
    fstore.create_project_schema()
    fstore.load_data("gs://continual-dev/testing_data/train1.csv", "tweets_raw")
    fstore.load_data("gs://continual-dev/testing_data/username.csv", "twitter_user_raw")
    fstore.load_data("gs://continual-dev/testing_data/bank_train.csv", "bank_train")

    # Note: The redshift examples work for databricks
    fstore.load("./examples/bank_marketing/redshift")
    mgmt_databricks = ManagementDummy(feature_store=fstore, project_id=project_id)

    print("Databricks featurestore ready")
    return mgmt_databricks


@pytest.fixture(scope="session")
def redshift_mgmt():
    print("Going to create redshift management")
    rs_datastore = get_redshift_datastore()
    mgmt_redshift = None
    if rs_datastore is None:
        return None

    project_id = "testproject_" + shortuuid.uuid().lower()
    fstore = get_featurestore(rs_datastore, projectid=project_id)
    fstore.cleanup()
    fstore.create_project_schema()
    fstore.load_data(
        "gs://continual-dev/testing_data/train1.csv", project_id, "tweets_raw"
    )
    fstore.load_data(
        "gs://continual-dev/testing_data/username.csv", project_id, "twitter_user_raw"
    )
    fstore.load_data(
        "gs://continual-dev/testing_data/bank_train.csv", project_id, "bank_train"
    )

    # Note: The bigquery examples work for redshift
    fstore.load("./examples/twitter/bigquery")
    fstore.load("./examples/bank_marketing/redshift")
    mgmt_redshift = ManagementDummy(feature_store=fstore, project_id=project_id)

    print("Redshift featurestore ready")
    return mgmt_redshift


def get_type_enum(typename):

    if typename is None:
        return None

    return management_types_pb2._FIELDTYPE.values_by_name[typename.upper()].number


def get_snowflake_datastore():
    if not os.path.isfile(TEST_CONFIG_FILE):
        print(
            "Test config file not found. Snowflake datastore not created ",
            __file__,
        )
        return None

    with open(TEST_CONFIG_FILE) as inp_file:
        cfg = yaml.load(inp_file, Loader=yaml.FullLoader)
        if "snowflake_connection" not in cfg:
            print(
                "Snowflake connection info not found in test configuration file, skipping ",
                __file__,
            )
            return None

        connection_info = cfg["snowflake_connection"]

        d = management_types_pb2.DataStore(
            type=connection_info["type"],
            snowflake=management_types_pb2.DataStore.Snowflake(
                username=connection_info["username"],
                database=connection_info["database"],
                password=connection_info["password"],
                host=connection_info["host"],
                warehouse=connection_info["warehouse"],
            ),
        )

        return d


def get_databricks_datastore():
    if not os.path.isfile(TEST_CONFIG_FILE):
        print(
            "Test config file not found. databricks datastore not created ",
            __file__,
        )
        return None

    with open(TEST_CONFIG_FILE) as inp_file:
        cfg = yaml.load(inp_file, Loader=yaml.FullLoader)
        if "databricks_connection" not in cfg:
            print(
                "Databricks connection info not found in test configuration file, skipping ",
                __file__,
            )
            return None

        connection_info = cfg["databricks_connection"]
        print(f"connection_info: {connection_info}")

        d = management_types_pb2.DataStore(
            type=connection_info["type"],
            databricks=management_types_pb2.DataStore.Databricks(
                http_path=connection_info["http_path"],
                database=connection_info["database"],
                token=connection_info["token"],
                host=connection_info["host"],
                port=connection_info["port"],
            ),
        )

        return d


def get_redshift_datastore():
    if not os.path.isfile(TEST_CONFIG_FILE):
        print(
            "Test config file not found. redshift datastore not created ",
            __file__,
        )
        return None

    with open(TEST_CONFIG_FILE) as inp_file:
        cfg = yaml.load(inp_file, Loader=yaml.FullLoader)
        if "redshift_connection" not in cfg:
            print(
                "Redshift connection info not found in test configuration file, skipping ",
                __file__,
            )
            return None

        connection_info = cfg["redshift_connection"]

        d = management_types_pb2.DataStore(
            type=connection_info["type"],
            redshift=management_types_pb2.DataStore.Redshift(
                username=connection_info["username"],
                database=connection_info["database"],
                password=connection_info["password"],
                host=connection_info["host"],
                port=connection_info["port"],
            ),
        )

        return d


def get_bigquery_datastore():
    if not os.path.isfile(TEST_CONFIG_FILE):
        print(
            "Test config file not found. Snowflake datastore not created ",
            __file__,
        )
        return None

    with open(TEST_CONFIG_FILE) as inp_file:
        cfg = yaml.load(inp_file, Loader=yaml.FullLoader)
        if "bigquery_credentials" not in cfg:
            print(
                "BigQuery credentials not found in test configuration file, skipping ",
                __file__,
            )
            return None

        connection_info = cfg["bigquery_credentials"]
        data = None
        with open(connection_info["cred_file"], "r") as fp:
            data = fp.read()

        d = management_types_pb2.DataStore(
            type="bigquery",
            big_query=management_types_pb2.DataStore.BigQuery(auth_file=data),
        )
        return d


def get_mssql_datastore():
    if not os.path.isfile(TEST_CONFIG_FILE):
        print(
            "Test config file not found. mssql datastore not created ",
            __file__,
        )
        return None

    with open(TEST_CONFIG_FILE) as inp_file:
        cfg = yaml.load(inp_file, Loader=yaml.FullLoader)
        if "mssql_connection" not in cfg:
            print(
                "Mssql connection info not found in test configuration file, skipping ",
                __file__,
            )
            pytest.skip(
                "Mssql connection info not found in test configuration file, skipping "
            )

        connection_info = cfg["mssql_connection"]

        d = management_types_pb2.DataStore(
            type=connection_info["type"],
            username=connection_info["username"],
            database=connection_info["database"],
            password=connection_info["password"],
            host=connection_info["host"],
            port=connection_info["port"],
        )
        return d


class ManagementDummy:
    def __init__(self, **kwargs):
        self.feature_sets = {}
        self.fs_store = kwargs["feature_store"]
        self.project_id = kwargs["project_id"]
        self.project_name = "projects/" + self.project_id

    def _get_latest_fs_name(self, name):
        latest_version = 0
        latest_version_name = None

        check_name = name.split("@")[0]
        for fs_name in self.feature_sets.keys():
            if fs_name.startswith(check_name):
                version = fs_name.split("@")[1]
                if version > latest_version:
                    latest_version = version
                    latest_version_name = fs_name

        return latest_version_name

    def PutFeatureSet(self, request):

        """
        Assignes a version and store the featureset.
        Currently only one version is supported.
        """
        featureSetname = request.parent + "/" + request.feature_set.schema.name
        request.feature_set.name = featureSetname

        fs = management_types_pb2.FeatureSet()
        fs.CopyFrom(request.feature_set)
        fs.name = featureSetname
        self.feature_sets[featureSetname] = fs

        self.fs_store.create_feature_table(fs)
        return request.feature_set

    def GetFeatureSet(self, request):

        """
        Returns the featureset with given name.
           TODO: Return the latest featureset if the version is not provided.
        """
        return self.feature_sets.get(request.name, None)

    def BatchGetFeatureSets(self, request):
        pass

    def GetFeatureSetMap(self):
        return self.feature_sets


def test_store(postgres_mgmt):
    featureset = management_types_pb2.FeatureSet()
    featureset.name = "projects/" + postgres_mgmt.project_id + "/featureSets/storetest"

    tab = postgres_mgmt.fs_store.get_feature_table(featureset)
    assert tab is None, "Feature table exists unexpectedely"


def create_project(mgmt):
    if mgmt is None:
        return

    print("create_project: " + mgmt.fs_store.get_type())
    project_id = "test123_" + shortuuid.uuid().lower()
    mgmt.fs_store.set_db_schema(project_id)

    mgmt.fs_store.create_project_schema()


def test_create_project(
    postgres_mgmt, snowflake_mgmt, bigquery_mgmt, redshift_mgmt, databricks_mgmt
):
    create_project(postgres_mgmt)
    create_project(snowflake_mgmt)
    create_project(bigquery_mgmt)
    create_project(redshift_mgmt)
    create_project(databricks_mgmt)


def compute_stats(mgmt):
    if mgmt is None:
        return
    print("compute_stats: " + mgmt.fs_store.get_type())

    name = "projects/" + mgmt.project_id + "/featureSets/bankmarketing"
    num_rows, computed_at, features = mgmt.fs_store.compute_feature_stats(
        name, mgmt.fs_store.featuresets[name].schema.columns
    )
    assert num_rows > 0, "compute stats failed"
    assert len(features) > 0, "compute stats failed"


def test_compute_stats(snowflake_mgmt, bigquery_mgmt, redshift_mgmt, databricks_mgmt):
    compute_stats(snowflake_mgmt)
    compute_stats(bigquery_mgmt)
    compute_stats(redshift_mgmt)
    compute_stats(databricks_mgmt)


def training_data(mgmt):
    if mgmt is None:
        return
    print("training_data: " + mgmt.fs_store.get_type())
    name = "projects/" + mgmt.project_id + "/models/bankmarketing_duration"

    dfi, query = mgmt.fs_store.get_training_data(
        mgmt.fs_store.models[name],
        featureset_map=mgmt.fs_store.featuresets,
        local=False,
        n=50_000,
    )
    try:
        df = next(dfi)
        print(df.shape)
        assert query, "get_training_data failed"
        assert df.shape[0] == 41188, "Unexpected number of rows returned"
    except StopIteration:
        assert False, "DId not get the dataframe rom the iterator"

    dfi, query = mgmt.fs_store.get_training_data(
        mgmt.fs_store.models[name],
        featureset_map=mgmt.fs_store.featuresets,
        n=10000,
        local=False,
    )
    done = False
    count = 0
    assert query, "get_training_data failed"
    while not done:
        try:
            df = next(dfi)
            assert df.shape[0] > 0, "Unexpected number of rows returned"
            assert df.shape[0] <= 10000, "Unexpected number of rows returned"
            count = count + 1
            assert count <= 5, "More iteration than expected"
        except:
            done = True

    assert count == 5, "More iteration than expected"


def test_get_training_data(
    snowflake_mgmt, bigquery_mgmt, redshift_mgmt, databricks_mgmt
):
    training_data(snowflake_mgmt)
    training_data(bigquery_mgmt)
    training_data(redshift_mgmt)
    training_data(databricks_mgmt)


def serving_data(mgmt):
    if mgmt is None:
        return
    print("serving_data: " + mgmt.fs_store.get_type())
    name = "projects/" + mgmt.project_id + "/models/bankmarketing_duration"

    dfi, query = mgmt.fs_store.get_training_data(
        mgmt.fs_store.models[name],
        featureset_map=mgmt.fs_store.featuresets,
        local=False,
    )
    df = next(dfi)
    assert query, "get_training_data failed"
    assert df.shape[0] == 41188, "Unexpected number of rows returned"

    data = mgmt.fs_store.fetch_serving_data(
        query,
        overrides={"id": "100"},
        data_store=mgmt.fs_store,
    )
    print(data.columns)
    assert data.shape[1] == 22, "Unexpected number of columns received"
    assert data.shape[0] == 1, "Unexpected number of columns received"

    """
    req = management_pb2.GetFeatureSetRequest(
        name="projects/" + mgmt.project_id + "/featureSets/tweet_rel"
    )
    mgmt.GetFeatureSet(req)
    all_featuresets = mgmt.GetFeatureSetMap()

    dfi, query = mgmt.fs_store.get_training_data("tweet_rel:rating", all_featuresets)
    df = next(dfi)
    assert query, "get_training_data failed"
    assert df.shape[0] == 999, "Unexpected number of rows returned"

    data = mgmt.fs_store.fetch_serving_data(
        query,
        overrides={"tweet_rel:id": "20"},
        data_store=mgmt.fs_store,
    )
    print(data)
    assert data.shape[1] == 10, "Unexpected number of columns received"
    assert data.shape[0] == 1, "Unexpected number of rows received"
    assert data["tweet_rel:id"][0] == "20"

    data = mgmt.fs_store.fetch_serving_data(
        query,
        overrides={"tweet_rel:id": "20", "tweet_rel:text": "Hope this works"},
        data_store=mgmt.fs_store,
    )
    assert data.shape[1] == 10, "Unexpected number of columns received"
    assert data.shape[0] == 1, "Unexpected number of rows received"
    assert data["tweet_rel:id"][0] == "20"
    assert data["tweet_rel:text"][0] == "Hope this works"

    data = mgmt.fs_store.fetch_serving_data(
        query,
        overrides={"tweet_rel:text": "Hope this works"},
        data_store=mgmt.fs_store,
    )
    assert data.shape[0] == 1, "Unexpected number of rows received"
    assert data["tweet_rel:text"][0] == "Hope this works"
    """


# def test_get_serving_data(snowflake_mgmt, bigquery_mgmt):
#    print("test_get_serving_data: ")
#    #serving_data(snowflake_mgmt)
#    serving_data(bigquery_mgmt)


def test_infer_schema_from_query_snowflake():
    data_store = get_snowflake_datastore()
    if data_store is None:
        print("Test configuration not found. skipping ")
        pytest.skip("Test configuration not found. skipping")

    env = management_types_pb2.Environment(
        name="projects/testproject", data_store=data_store
    )
    req = dataingest_pb2.GetInferredSchemaRequest(
        environment=env,
        query='SELECT id, TO_NUMBER(id, 6) as intid, text, rating  from  "CONTINUAL".featurestore_test.tweets order by intid',
    )

    os.environ["CONFIG_ENV"] = "local"
    server = DataIngestService()

    resp = server.GetInferredSchema(req, None)

    print("number of features found ", str(len(resp.columns)))
    print("sample data size", resp.record_count)

    assert len(resp.columns) == 4, "Unexpected number of features inferred"
    assert resp.record_count > 0, "No sample data returned"

    req = dataingest_pb2.GetInferredSchemaRequest(
        environment=env,
        query='SELECT id, TO_NUMBER(id, 6) as intid, text, rating  from  "CONTINUAL".featurestore_test.tweets order by intid',
    )

    resp = server.GetInferredSchema(req, None)

    assert len(resp.columns) == 4, "Unexpected number of features inferred"
    assert resp.record_count > 0, "No sample data returned"


def test_infer_schema_from_query_bigquery():
    data_store = get_bigquery_datastore()
    if data_store is None:
        print("Test configuration not found. skipping ")
        pytest.skip("Test configuration not found. skipping")

    fstore = get_featurestore(data_store, projectid="testproject")
    fstore.create_project_schema()

    env = management_types_pb2.Environment(
        name="projects/testproject", data_store=data_store
    )
    req = dataingest_pb2.GetInferredSchemaRequest(
        environment=env,
        query="SELECT id, CAST(id as STRING) as strid, text, rating  from  featurestore_test.tweets order by id",
    )

    os.environ["CONFIG_ENV"] = "local"
    server = DataIngestService()

    resp = server.GetInferredSchema(req, None)

    print("number of features found ", str(len(resp.columns)))
    print("sample data size", resp.record_count)

    assert len(resp.columns) == 4, "Unexpected number of features inferred"
    assert resp.record_count > 0, "No sample data returned"

    req = dataingest_pb2.GetInferredSchemaRequest(
        environment=env,
        query="SELECT id, CAST(id as STRING) as strid, text, rating  from  featurestore_test.tweets order by id",
    )

    resp = server.GetInferredSchema(req, None)

    assert len(resp.columns) == 4, "Unexpected number of features inferred"
    assert resp.record_count > 0, "No sample data returned"


def test_infer_schema_from_query_redshift():
    data_store = get_redshift_datastore()
    if data_store is None:
        print("Test configuration not found. skipping ")
        pytest.skip("Test configuration not found. skipping")

    fstore = get_featurestore(data_store, projectid="testproject")
    fstore.create_project_schema()

    env = management_types_pb2.Environment(
        name="projects/testproject", data_store=data_store
    )
    req = dataingest_pb2.GetInferredSchemaRequest(
        environment=env,
        query="SELECT id, CAST(id as char) as idstr, text, rating  from  featurestore_test.tweets order by id",
    )

    os.environ["CONFIG_ENV"] = "local"
    server = DataIngestService()

    resp = server.GetInferredSchema(req, None)

    print("number of features found ", str(len(resp.columns)))
    print("sample data size", resp.record_count)

    assert len(resp.columns) == 4, "Unexpected number of features inferred"
    assert resp.record_count > 0, "No sample data returned"

    req = dataingest_pb2.GetInferredSchemaRequest(
        environment=env,
        query="SELECT id,  CAST(id as char) as idstr, text, rating  from  featurestore_test.tweets order by id",
    )

    resp = server.GetInferredSchema(req, None)

    assert len(resp.columns) == 4, "Unexpected number of features inferred"
    assert resp.record_count > 0, "No sample data returned"


def test_infer_schema_from_query_databricks():
    data_store = get_databricks_datastore()
    if data_store is None:
        print("Test configuration not found. skipping ")
        pytest.skip("Test configuration not found. skipping")

    fstore = get_featurestore(data_store, projectid="testproject")
    if not fstore.data_store.databricks.db_schema:
        fstore.db_schema = "testproject"
    fstore.create_project_schema()

    env = management_types_pb2.Environment(
        name="projects/testproject", data_store=data_store
    )
    req = dataingest_pb2.GetInferredSchemaRequest(
        environment=env,
        query="SELECT id, CAST(id as string) as idstr, text, rating  from  featurestore_test.tweets order by id",
    )

    os.environ["CONFIG_ENV"] = "local"
    server = DataIngestService()

    resp = server.GetInferredSchema(req, None)

    print("number of features found ", str(len(resp.columns)))
    print("sample data size", resp.record_count)

    assert len(resp.columns) == 4, "Unexpected number of features inferred"
    assert resp.record_count > 0, "No sample data returned"

    req = dataingest_pb2.GetInferredSchemaRequest(
        environment=env,
        query="SELECT id,  CAST(id as string) as idstr, text, rating  from  featurestore_test.tweets order by id",
    )

    resp = server.GetInferredSchema(req, None)

    assert len(resp.columns) == 4, "Unexpected number of features inferred"
    assert resp.record_count > 0, "No sample data returned"

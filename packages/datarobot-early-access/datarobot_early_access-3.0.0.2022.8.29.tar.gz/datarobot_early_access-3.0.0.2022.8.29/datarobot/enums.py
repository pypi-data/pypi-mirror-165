#
# Copyright 2021-2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.


def enum(*vals, **enums):
    """
    Enum without third party libs and compatible with py2 and py3 versions.
    """
    enums.update(dict(zip(vals, vals)))
    return type("Enum", (), enums)


CV_METHOD = enum(
    DATETIME="datetime",
    GROUP="group",
    RANDOM="random",
    STRATIFIED="stratified",
    USER="user",
)


class PROJECT_CV_METHOD:
    DATETIME = "DatetimeCV"
    GROUP = "GroupCV"
    RANDOM = "RandomCV"
    STRATIFIED = "StratifiedCV"
    USER = "UserCV"
    ALL = [DATETIME, GROUP, RANDOM, STRATIFIED, USER]


class VALIDATION_TYPE:
    CV = "CV"
    TVH = "TVH"
    ALL = [CV, TVH]


SCORING_TYPE = enum(cross_validation="crossValidation", validation="validation")

DATETIME_AUTOPILOT_DATA_SELECTION_METHOD = enum(DURATION="duration", ROW_COUNT="rowCount")
DATETIME_AUTOPILOT_DATA_SAMPLING_METHOD = enum(LATEST="latest", RANDOM="random")

VERBOSITY_LEVEL = enum(SILENT=0, VERBOSE=2)

# This is deprecated, to be removed in 3.0.
MODEL_JOB_STATUS = enum(ERROR="error", INPROGRESS="inprogress", QUEUE="queue")

# This is the job/queue status enum we want to keep.
# In 3.0 this will be INITIALIZED, RUNNING, ABORTED, COMPLETED, ERROR.
# And maybe the name will change to JobStatus.
QUEUE_STATUS = enum(
    ABORTED="ABORTED",
    COMPLETED="COMPLETED",
    ERROR="error",
    INPROGRESS="inprogress",
    QUEUE="queue",
    RUNNING="RUNNING",
    INITIALIZING="INITIALIZING",
)

AUTOPILOT_MODE = enum(
    FULL_AUTO="auto",
    MANUAL="manual",
    QUICK="quick",
    COMPREHENSIVE="comprehensive",
)

PROJECT_STAGE = enum(
    AIM="aim", EDA="eda", EDA2="eda2", FASTEDA="fasteda", EMPTY="empty", MODELING="modeling"
)

ASYNC_PROCESS_STATUS = enum(
    ABORTED="ABORTED",
    COMPLETED="COMPLETED",
    ERROR="ERROR",
    INITIALIZED="INITIALIZED",
    RUNNING="RUNNING",
)

LEADERBOARD_SORT_KEY = enum(PROJECT_METRIC="metric", SAMPLE_PCT="samplePct")


class TARGET_TYPE:
    BINARY = "Binary"
    MULTICLASS = "Multiclass"
    MULTILABEL = "Multilabel"
    REGRESSION = "Regression"
    UNSTRUCTURED = "Unstructured"
    ANOMALY = "Anomaly"
    ALL = [BINARY, MULTICLASS, MULTILABEL, REGRESSION, UNSTRUCTURED, ANOMALY]


JOB_TYPE = enum(
    BATCH_PREDICTIONS="batchPredictions",
    BATCH_PREDICTION_JOB_DEFINITIONS="batchPredictionJobDefinitions",
    FEATURE_IMPACT="featureImpact",
    FEATURE_EFFECTS="featureEffects",
    FEATURE_FIT="featureFit",
    MODEL="model",
    MODEL_EXPORT="modelExport",
    PREDICT="predict",
    TRAINING_PREDICTIONS="trainingPredictions",
    PRIME_MODEL="primeModel",
    PRIME_RULESETS="primeRulesets",
    PRIME_VALIDATION="primeDownloadValidation",
    PREDICTION_EXPLANATIONS="predictionExplanations",
    PREDICTION_EXPLANATIONS_INITIALIZATION="predictionExplanationsInitialization",
    RATING_TABLE_VALIDATION="validateRatingTable",
    SHAP_IMPACT="shapImpact",
)

PREDICT_JOB_STATUS = enum(ABORTED="ABORTED", ERROR="error", INPROGRESS="inprogress", QUEUE="queue")

PREDICTION_PREFIX = enum(DEFAULT="class_")

PRIME_LANGUAGE = enum(JAVA="Java", PYTHON="Python")

VARIABLE_TYPE_TRANSFORM = enum(
    CATEGORICAL_INT="categoricalInt",
    NUMERIC="numeric",
    TEXT="text",
)

DATE_EXTRACTION = enum(
    MONTH="month",
    MONTH_DAY="monthDay",
    WEEK="week",
    WEEK_DAY="weekDay",
    YEAR="year",
    YEAR_DAY="yearDay",
)

POSTGRESQL_DRIVER = enum(ANSI="PostgreSQL ANSI", UNICODE="PostgreSQL Unicode")

BLENDER_METHOD = enum(
    AVERAGE="AVG",
    ENET="ENET",
    GLM="GLM",
    MAE="MAE",
    MAEL1="MAEL1",
    MEDIAN="MED",
    PLS="PLS",
    RANDOM_FOREST="RF",
    LIGHT_GBM="LGBM",
    TENSORFLOW="TF",
    FORECAST_DISTANCE_ENET="FORECAST_DISTANCE_ENET",
    FORECAST_DISTANCE_AVG="FORECAST_DISTANCE_AVG",
)

TS_BLENDER_METHOD = enum(
    AVERAGE="AVG",
    MEDIAN="MED",
    FORECAST_DISTANCE_ENET="FORECAST_DISTANCE_ENET",
    FORECAST_DISTANCE_AVG="FORECAST_DISTANCE_AVG",
)

CHART_DATA_SOURCE = enum(
    CROSSVALIDATION="crossValidation",
    HOLDOUT="holdout",
    VALIDATION="validation",
)

DATA_SUBSET = enum(
    ALL="all",
    VALIDATION_AND_HOLDOUT="validationAndHoldout",
    HOLDOUT="holdout",
    ALL_BACKTESTS="allBacktests",
)

FEATURE_TYPE = enum(NUMERIC="numeric", CATEGORICAL="categorical", DATETIME="datetime")

DEFAULT_MAX_WAIT = 600

# default time out values in seconds for waiting response from client
DEFAULT_TIMEOUT = enum(
    CONNECT=6.05,  # time in seconds for the connection to server to be established
    READ=60,  # time in seconds after which to conclude the server isn't responding anymore
    UPLOAD=600,  # time in seconds after which to conclude that project dataset cannot be uploaded
)

# Time in seconds after which to conclude the server isn't responding anymore
# same as in DEFAULT_TIMEOUT, keeping for backwards compatibility
DEFAULT_READ_TIMEOUT = DEFAULT_TIMEOUT.READ

TARGET_LEAKAGE_TYPE = enum(
    SKIPPED_DETECTION="SKIPPED_DETECTION",
    FALSE="FALSE",
    MODERATE_RISK="MODERATE_RISK",
    HIGH_RISK="HIGH_RISK",
)


class TREAT_AS_EXPONENTIAL:
    ALWAYS = "always"
    NEVER = "never"
    AUTO = "auto"
    ALL = [ALWAYS, NEVER, AUTO]


DIFFERENCING_METHOD = enum(AUTO="auto", SIMPLE="simple", NONE="none", SEASONAL="seasonal")


class TIME_UNITS:
    """
    Available time units that may be returned by the API
    """

    MILLISECOND = "MILLISECOND"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"
    ALL = [MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR]


PERIODICITY_MAX_TIME_STEP = 9223372036854775807

RECOMMENDED_MODEL_TYPE = enum(
    MOST_ACCURATE="Most Accurate",
    FAST_ACCURATE="Fast & Accurate",
    RECOMMENDED_FOR_DEPLOYMENT="Recommended for Deployment",
)

AVAILABLE_STATEMENT_TYPES = enum(
    INSERT="insert",
    UPDATE="update",
    INSERT_UPDATE="insert_update",
    CREATE_TABLE="create_table",
)


class _DEPLOYMENT_HEALTH_STATUS:
    PASSING = "passing"
    WARNING = "warning"
    FAILING = "failing"
    UNKNOWN = "unknown"

    ALL = [PASSING, WARNING, FAILING, UNKNOWN]


class DEPLOYMENT_SERVICE_HEALTH_STATUS(_DEPLOYMENT_HEALTH_STATUS):
    pass


class DEPLOYMENT_MODEL_HEALTH_STATUS(_DEPLOYMENT_HEALTH_STATUS):
    pass


class DEPLOYMENT_ACCURACY_HEALTH_STATUS(_DEPLOYMENT_HEALTH_STATUS):
    UNAVAILABLE = "unavailable"

    ALL = _DEPLOYMENT_HEALTH_STATUS.ALL + [UNAVAILABLE]


class DEPLOYMENT_EXECUTION_ENVIRONMENT_TYPE:
    DATAROBOT = "datarobot"
    EXTERNAL = "external"

    ALL = [DATAROBOT, EXTERNAL]


class DEPLOYMENT_IMPORTANCE:
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LOW = "LOW"

    ALL = [CRITICAL, HIGH, MODERATE, LOW]


SERIES_AGGREGATION_TYPE = enum(AVERAGE="average", TOTAL="total")

MONOTONICITY_FEATURELIST_DEFAULT = object()

SERIES_ACCURACY_ORDER_BY = enum(
    MULTISERIES_VALUE="multiseriesValue",
    ROW_COUNT="rowCount",
    VALIDATION_SCORE="validationScore",
    BACKTESTING_SCORE="backtestingScore",
    HOLDOUT_SCORE="holdoutScore",
)

SHARING_ROLE = enum(
    OWNER="OWNER",
    READ_WRITE="READ_WRITE",
    USER="USER",
    EDITOR="EDITOR",
    READ_ONLY="READ_ONLY",
    CONSUMER="CONSUMER",
)

MODEL_REPLACEMENT_REASON = enum(
    ACCURACY="ACCURACY",
    DATA_DRIFT="DATA_DRIFT",
    ERRORS="ERRORS",
    SCHEDULED_REFRESH="SCHEDULED_REFRESH",
    SCORING_SPEED="SCORING_SPEED",
    OTHER="OTHER",
)

EXPLANATIONS_ALGORITHM = enum(SHAP="shap")


class FEATURE_ASSOCIATION_TYPE:
    ASSOCIATION = "association"
    CORRELATION = "correlation"

    ALL = [ASSOCIATION, CORRELATION]


class FEATURE_ASSOCIATION_METRIC:
    # association
    MUTUAL_INFO = "mutualInfo"
    CRAMER = "cramersV"
    # correlation
    SPEARMAN = "spearman"
    PEARSON = "pearson"
    TAU = "tau"

    ALL = [MUTUAL_INFO, CRAMER, SPEARMAN, PEARSON, TAU]


class SERVICE_STAT_METRIC:  # pylint: disable=missing-class-docstring
    TOTAL_PREDICTIONS = "totalPredictions"
    TOTAL_REQUESTS = "totalRequests"
    SLOW_REQUESTS = "slowRequests"
    EXECUTION_TIME = "executionTime"
    RESPONSE_TIME = "responseTime"
    USER_ERROR_RATE = "userErrorRate"
    SERVER_ERROR_RATE = "serverErrorRate"
    NUM_CONSUMERS = "numConsumers"
    CACHE_HIT_RATIO = "cacheHitRatio"
    MEDIAN_LOAD = "medianLoad"
    PEAK_LOAD = "peakLoad"

    ALL = [
        TOTAL_PREDICTIONS,
        TOTAL_REQUESTS,
        SLOW_REQUESTS,
        EXECUTION_TIME,
        RESPONSE_TIME,
        USER_ERROR_RATE,
        SERVER_ERROR_RATE,
        NUM_CONSUMERS,
        CACHE_HIT_RATIO,
        MEDIAN_LOAD,
        PEAK_LOAD,
    ]


class DATA_DRIFT_METRIC:
    PSI = "psi"
    KL_DIVERGENCE = "kl_divergence"
    DISSIMILARITY = "dissimilarity"
    HELLINGER = "hellinger"
    JS_DIVERGENCE = "js_divergence"
    ALL = [PSI, KL_DIVERGENCE, DISSIMILARITY, HELLINGER, JS_DIVERGENCE]


class ACCURACY_METRIC:  # pylint: disable=missing-class-docstring
    ACCURACY = "Accuracy"
    AUC = "AUC"
    BALANCED_ACCURACY = "Balanced Accuracy"
    FVE_BINOMIAL = "FVE Binomial"
    GINI_NORM = "Gini Norm"
    KOLMOGOROV_SMIRNOV = "Kolmogorov-Smirnov"
    LOGLOSS = "LogLoss"
    RATE_TOP5 = "Rate@Top5%"
    RATE_TOP10 = "Rate@Top10%"
    TPR = "TPR"
    PPV = "PPV"
    F1 = "F1"
    MCC = "MCC"

    GAMMA_DEVIANCE = "Gamma Deviance"
    FVE_GAMMA = "FVE Gamma"
    FVE_POISSON = "FVE Poisson"
    FVE_TWEEDIE = "FVE Tweedie"
    MAD = "MAD"
    MAE = "MAE"
    MAPE = "MAPE"
    POISSON_DEVIANCE = "Poisson Deviance"
    R_SQUARED = "R Squared"
    RMSE = "RMSE"
    RMSLE = "RMSLE"
    TWEEDIE_DEVIANCE = "Tweedie Deviance"

    ALL_CLASSIFICATION = [
        ACCURACY,
        AUC,
        BALANCED_ACCURACY,
        FVE_BINOMIAL,
        GINI_NORM,
        KOLMOGOROV_SMIRNOV,
        LOGLOSS,
        RATE_TOP5,
        RATE_TOP10,
        TPR,
        PPV,
        F1,
        MCC,
    ]
    ALL_REGRESSION = [
        GAMMA_DEVIANCE,
        FVE_GAMMA,
        FVE_POISSON,
        FVE_TWEEDIE,
        MAD,
        MAE,
        MAPE,
        POISSON_DEVIANCE,
        R_SQUARED,
        RMSE,
        RMSLE,
        TWEEDIE_DEVIANCE,
    ]
    ALL = [
        ACCURACY,
        AUC,
        BALANCED_ACCURACY,
        FVE_BINOMIAL,
        GINI_NORM,
        KOLMOGOROV_SMIRNOV,
        LOGLOSS,
        RATE_TOP5,
        RATE_TOP10,
        GAMMA_DEVIANCE,
        FVE_GAMMA,
        FVE_POISSON,
        FVE_TWEEDIE,
        MAD,
        MAE,
        MAPE,
        POISSON_DEVIANCE,
        R_SQUARED,
        RMSE,
        RMSLE,
        TWEEDIE_DEVIANCE,
        TPR,
        PPV,
        F1,
        MCC,
    ]


class EXECUTION_ENVIRONMENT_VERSION_BUILD_STATUS:
    """Enum of possible build statuses of execution environment version."""

    SUBMITTED = "submitted"
    PROCESSING = "processing"
    FAILED = "failed"
    SUCCESS = "success"

    FINAL_STATUSES = [FAILED, SUCCESS]


class CUSTOM_MODEL_IMAGE_TYPE:
    """Enum of types that can represent a custom model image"""

    CUSTOM_MODEL_VERSION = "customModelVersion"
    CUSTOM_MODEL_IMAGE = "customModelImage"

    ALL = [CUSTOM_MODEL_IMAGE, CUSTOM_MODEL_VERSION]


class _SHARED_TARGET_TYPE:
    """Enum of all target types shared by tasks and models"""

    BINARY = "Binary"
    ANOMALY = "Anomaly"
    REGRESSION = "Regression"
    MULTICLASS = "Multiclass"
    ALL = [BINARY, ANOMALY, REGRESSION, MULTICLASS]


class CUSTOM_MODEL_TARGET_TYPE(_SHARED_TARGET_TYPE):
    """Enum of valid custom model target types"""

    UNSTRUCTURED = "Unstructured"
    REQUIRES_TARGET_NAME = ("Binary", "Multiclass", "Regression")

    ALL = _SHARED_TARGET_TYPE.ALL + [UNSTRUCTURED]


class CUSTOM_TASK_TARGET_TYPE(_SHARED_TARGET_TYPE):
    """Enum of valid custom task target types"""

    TRANSFORM = "Transform"

    ALL = _SHARED_TARGET_TYPE.ALL + [TRANSFORM]


class NETWORK_EGRESS_POLICY:
    """Enum of valid network egress policy"""

    NONE = "NONE"
    PUBLIC = "PUBLIC"

    ALL = [NONE, PUBLIC]


class SOURCE_TYPE:
    """Enum of backtest source types"""

    TRAINING = "training"
    VALIDATION = "validation"

    ALL = [TRAINING, VALIDATION]


class DATETIME_TREND_PLOTS_STATUS:
    COMPLETED = "completed"
    NOT_COMPLETED = "notCompleted"
    IN_PROGRESS = "inProgress"
    ERRORED = "errored"
    NOT_SUPPORTED = "notSupported"
    INSUFFICIENT_DATA = "insufficientData"

    ALL = [COMPLETED, NOT_COMPLETED, IN_PROGRESS, ERRORED, NOT_SUPPORTED, INSUFFICIENT_DATA]


class DATETIME_TREND_PLOTS_RESOLUTION:  # pylint: disable=missing-class-docstring
    MILLISECONDS = "milliseconds"
    SECONDS = "seconds"
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"
    MONTHS = "months"
    QUARTERS = "quarters"
    YEARS = "years"

    ALL = (
        MILLISECONDS,
        SECONDS,
        MINUTES,
        HOURS,
        DAYS,
        WEEKS,
        MONTHS,
        QUARTERS,
        YEARS,
    )


SNAPSHOT_POLICY = enum(SPECIFIED="specified", LATEST="latest", DYNAMIC="dynamic")


class AllowedTimeUnitsSAFER:
    """Enum for SAFER allowed time units"""

    MILLISECOND = "MILLISECOND"
    SECOND = "SECOND"
    MINUTE = "MINUTE"
    HOUR = "HOUR"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    QUARTER = "QUARTER"
    YEAR = "YEAR"

    ALL = (MILLISECOND, SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, QUARTER, YEAR)


class FeatureDiscoveryMode:
    DEFAULT = "default"
    MANUAL = "manual"
    ALL = (DEFAULT, MANUAL)


class AnomalyAssessmentStatus:
    COMPLETED = "completed"
    NO_DATA = "noData"  # when there is no series in backtest/source
    NOT_SUPPORTED = "notSupported"  # when full training subset can not be fit into memory.

    ALL = (COMPLETED, NO_DATA, NOT_SUPPORTED)


class UnsupervisedTypeEnum:
    ANOMALY = "anomaly"
    CLUSTERING = "clustering"


class FairnessMetricsSet:
    PROPORTIONAL_PARITY = "proportionalParity"
    EQUAL_PARITY = "equalParity"
    PREDICTION_BALANCE = "predictionBalance"
    TRUE_FAVORABLE_AND_UNFAVORABLE_RATE_PARITY = "trueFavorableAndUnfavorableRateParity"
    FAVORABLE_AND_UNFAVORABLE_PREDICTIVE_VALUE_PARITY = (
        "favorableAndUnfavorablePredictiveValueParity"
    )

    ALL = (
        PROPORTIONAL_PARITY,
        EQUAL_PARITY,
        PREDICTION_BALANCE,
        TRUE_FAVORABLE_AND_UNFAVORABLE_RATE_PARITY,
        FAVORABLE_AND_UNFAVORABLE_PREDICTIVE_VALUE_PARITY,
    )


class FileLocationType:
    PATH = "path"
    URL = "url"
    ALL = [PATH, URL]


class LocalSourceType:
    DATA_FRAME = "DataFrame"
    FILELIKE = "filelike"


class ImageFormat:
    JPEG = "JPEG"
    PNG = "PNG"
    BMP = "BMP"
    PPM = "PPM"
    GIF = "GIF"
    MPO = "MPO"
    TIFF = "TIFF"
    ALL = [JPEG, PNG, BMP, PPM, GIF, MPO, TIFF]


# enum representing resample methods in alignment with PIL.Image resampling methods.
# Enum is created explicitly both for user convenience and because PIL library
# installation is optional dependency for datarobot library.
class ImageResampleMethod:
    NEAREST = NONE = 0
    LANCZOS = ANTIALIAS = 1
    BILINEAR = LINEAR = 2
    BICUBIC = CUBIC = 3
    BOX = 4
    HAMMING = 5


# Defaults used for image transformations preprocessing
# Image resize defaults
DEFAULT_VISUAL_AI_SHOULD_RESIZE = True
DEFAULT_VISUAL_AI_FORCE_SIZE = False
DEFAULT_VISUAL_AI_IMAGE_SIZE = (224, 224)
# Image format defaults
DEFAULT_VISUAL_AI_IMAGE_FORMAT = None  # preserve original image format
DEFAULT_VISUAL_AI_IMAGE_SUBSAMPLING = None  # uses Pillow library default
DEFAULT_VISUAL_AI_IMAGE_QUALITY_KEEP_IF_POSSIBLE = True
DEFAULT_VISUAL_AI_IMAGE_QUALITY = 75
DEFAULT_VISUAL_AI_IMAGE_RESAMPLE_METHOD = ImageResampleMethod.LANCZOS

# Image formats supported by DataRobot application
SUPPORTED_IMAGE_FORMATS = set(ImageFormat.ALL)


class BiasMitigationTechnique:
    PREPROCESSING_REWEIGHING = "preprocessingReweighing"
    POSTPROCESSING_REJECTION_OPTION = "postProcessingRejectionOptionBasedClassification"


class AuthenticationType:
    BASIC = "user" and "password"
    CREDENTIAL_ID = "credential_id"
    CREDENTIAL_DATA = "credential_data"
    ALL = [BASIC, CREDENTIAL_ID, CREDENTIAL_DATA]

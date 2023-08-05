import fdrtd
import fdrtd.server.exceptions


def create(microprotocol):

    if microprotocol == 'MinimumMaximum':
        from fdrtd.plugins.simon.microprotocols.microprotocol_minimum_maximum import MicroprotocolMinimumMaximum
        return MicroprotocolMinimumMaximum

    if microprotocol == 'SecureSum':
        from fdrtd.plugins.simon.microprotocols.microprotocol_secure_sum import MicroprotocolSecureSum
        return MicroprotocolSecureSum

    if microprotocol == 'SecureMatrixMultiplication':
        from fdrtd.plugins.simon.microprotocols.microprotocol_secure_matrix_multiplication import MicroprotocolSecureMatrixMultiplication
        return MicroprotocolSecureMatrixMultiplication

    if microprotocol == 'SetIntersection':
        from fdrtd.plugins.simon.microprotocols.microprotocol_set_intersection import MicroprotocolSetIntersection
        return MicroprotocolSetIntersection

    if microprotocol == 'SetIntersectionSize':
        from fdrtd.plugins.simon.microprotocols.microprotocol_set_intersection_size import MicroprotocolSetIntersectionSize
        return MicroprotocolSetIntersectionSize

    if microprotocol == 'StatisticsBivariate':
        from fdrtd.plugins.simon.microprotocols.microprotocol_statistics_bivariate import MicroprotocolStatisticsBivariate
        return MicroprotocolStatisticsBivariate

    if microprotocol == 'StatisticsFrequency':
        from fdrtd.plugins.simon.microprotocols.microprotocol_statistics_frequency import MicroprotocolStatisticsFrequency
        return MicroprotocolStatisticsFrequency

    if microprotocol == 'StatisticsContingency':
        from fdrtd.plugins.simon.microprotocols.microprotocol_statistics_contingency import MicroprotocolStatisticsContingency
        return MicroprotocolStatisticsContingency

    if microprotocol == 'StatisticsUnivariate':
        from fdrtd.plugins.simon.microprotocols.microprotocol_statistics_univariate import MicroprotocolStatisticsUnivariate
        return MicroprotocolStatisticsUnivariate

    if microprotocol == 'StatisticsContingencyVertical':
        from fdrtd.plugins.simon.microprotocols.microprotocol_statistics_contingency_vertical import MicroprotocolStatisticsContingencyVertical
        return MicroprotocolStatisticsContingencyVertical

    if microprotocol == 'StatisticsRegressionOLSVertical':
        from fdrtd.plugins.simon.microprotocols.microprotocol_statistics_regression_ols_vertical import MicroprotocolStatisticsRegressionOLSVertical
        return MicroprotocolStatisticsRegressionOLSVertical

    raise fdrtd.server.exceptions.NotAvailable(microprotocol)

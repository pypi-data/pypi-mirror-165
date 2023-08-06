"""
 #####
#     #  ####   ####  #   ##   #      #      #   #
#       #    # #    # #  #  #  #      #       # #
 #####  #    # #      # #    # #      #        #
      # #    # #      # ###### #      #        #
#     # #    # #    # # #    # #      #        #
 #####   ####   ####  # #    # ###### ######   #

######
#     # ###### ##### ###### #####  #    # # #    # ###### #####
#     # #        #   #      #    # ##  ## # ##   # #      #    #
#     # #####    #   #####  #    # # ## # # # #  # #####  #    #
#     # #        #   #      #####  #    # # #  # # #      #    #
#     # #        #   #      #   #  #    # # #   ## #      #    #
######  ######   #   ###### #    # #    # # #    # ###### #####
"""

"""
This module contains matching rules and methods
"""


from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as f
from pyspark.sql import types as t
from fuzzywuzzy import fuzz
from functools import reduce
from operator import add


class SDMatcher(object):
    """
    Class provides functionality for matching datasets on a variety of rules

    Creates matching object informed on roster. Provides methods for matching
    roster to enriched data sources

    Attributes:
        __required_cols (list[str]): Column definitions required for matching
        df (DataFrame): Session object from the boto3 Session class.
        roster_map (dict): Column map for roster df
    """

    def __init__(self, roster_df: dict, roster_map: dict):
        """
        Constructor

        Args:
            roster_df (DataFrame): DataFrame housing the initial roster
            roster_map (dict): Column Mapping from names to meaning
        """

        self._required_cols = [
            "id",
            "first_name",
            "last_name",
            "dob",
            "mob",
            "yob",
            "lat",
            "long",
        ]

        if not all([x in roster_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in roster column map")

        self.df = roster_df
        self.roster_map = roster_map

    def roster_exact_join(
        self, data_df: DataFrame, data_map: dict, join_conditions=[], use_dob=True
    ):
        """ Helper method for joining roster to data enriched dataframe based on join criteria

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns
            join_conditions (list): List of join key combinations
            use_dob (Boolean): Whether or not to join with birthdate

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        birth_date_join_conditions = [
            self.df[self.roster_map["yob"]] == data_df[data_map["yob"]],
            self.df[self.roster_map["mob"]] == data_df[data_map["mob"]],
            self.df[self.roster_map["dob"]] == data_df[data_map["dob"]],
        ]

        birth_date_join_filters = [
            f.col(data_map["mob"]).isNull() & f.col(data_map["dob"]).isNull(),
            f.col(data_map["mob"]).isNotNull() & f.col(data_map["dob"]).isNull(),
            f.col(data_map["mob"]).isNotNull() & f.col(data_map["dob"]).isNotNull(),
        ]

        if not use_dob:
            birth_date_join_conditions = []

        dfs = []
        for i in range(3):
            dfs.append(
                self.df.join(
                    data_df.filter(birth_date_join_filters[i]),
                    join_conditions + birth_date_join_conditions[: i + 1],
                    "inner",
                )
            )

        matches_df = reduce(DataFrame.union, dfs)
        return matches_df

    def r1(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 1 (First Name, Last Name, DOB)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        join_conditions = [
            self.df[self.roster_map["first_name"]] == data_df[data_map["first_name"]],
            self.df[self.roster_map["last_name"]] == data_df[data_map["last_name"]],
        ]

        matches_df = self.roster_exact_join(data_df, data_map, join_conditions)
        return matches_df

    def r2(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 2 (First 3 First Name, First 3 Last Name, DOB)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        join_conditions = [
            f.substring(self.df[self.roster_map["first_name"]], 0, 3)
            == f.substring(data_df[data_map["first_name"]], 0, 3),
            f.substring(self.df[self.roster_map["last_name"]], 0, 3)
            == f.substring(data_df[data_map["last_name"]], 0, 3),
        ]

        matches_df = self.roster_exact_join(data_df, data_map, join_conditions)
        return matches_df

    def r3(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 3 (First Name, DOB, 3 Digit Lat/Long)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        join_conditions = [
            self.df[self.roster_map["first_name"]] == data_df[data_map["first_name"]],
            f.round(self.df[self.roster_map["lat"]], 3) == f.round(data_df[data_map["lat"]], 3),
            f.round(self.df[self.roster_map["long"]], 3) == f.round(data_df[data_map["long"]], 3),
        ]

        matches_df = self.roster_exact_join(data_df, data_map, join_conditions)
        return matches_df

    def r4(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 4 (Last Name, DOB, 3 Digit Lat/Long)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        join_conditions = [
            self.df[self.roster_map["last_name"]] == data_df[data_map["last_name"]],
            f.round(self.df[self.roster_map["lat"]], 3) == f.round(data_df[data_map["lat"]], 3),
            f.round(self.df[self.roster_map["long"]], 3) == f.round(data_df[data_map["long"]], 3),
        ]

        matches_df = self.roster_exact_join(data_df, data_map, join_conditions)
        return matches_df

    def r5(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 5 (First Name, DOB, 2 Digit Lat/Long)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        join_conditions = [
            self.df[self.roster_map["first_name"]] == data_df[data_map["first_name"]],
            f.round(self.df[self.roster_map["lat"]], 2) == f.round(data_df[data_map["lat"]], 2),
            f.round(self.df[self.roster_map["long"]], 2) == f.round(data_df[data_map["long"]], 2),
        ]

        matches_df = self.roster_exact_join(data_df, data_map, join_conditions)
        return matches_df

    def r6(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 6 (Last Name, DOB, 2 Digit Lat/Long)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        join_conditions = [
            self.df[self.roster_map["last_name"]] == data_df[data_map["last_name"]],
            f.round(self.df[self.roster_map["lat"]], 2) == f.round(data_df[data_map["lat"]], 2),
            f.round(self.df[self.roster_map["long"]], 2) == f.round(data_df[data_map["long"]], 2),
        ]

        matches_df = self.roster_exact_join(data_df, data_map, join_conditions)
        return matches_df

    def r7(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 7 (Fuzzy 90 First Name, Fuzzy 90 Last Name, DOB)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        matches_df = self.roster_exact_join(data_df, data_map)

        @f.udf("int")
        def FuzzyMatchUDF(a, b):
            return fuzz.ratio(a, b)

        matches_df = matches_df.withColumn(
            "fuzzy_first_name_ratio",
            FuzzyMatchUDF(f.col(self.roster_map["first_name"]), f.col(data_map["first_name"])),
        ).withColumn(
            "fuzzy_last_name_ratio",
            FuzzyMatchUDF(f.col(self.roster_map["last_name"]), f.col(data_map["last_name"])),
        )

        thresh = 90
        matches_df = matches_df.filter(
            f"fuzzy_first_name_ratio >= {thresh} and fuzzy_last_name_ratio >= {thresh}"
        )
        return matches_df

    def r8(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 8 (Fuzzy 95 First Name, Fuzzy 95 Last Name, DOB)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        matches_df = self.roster_exact_join(data_df, data_map)

        @f.udf("int")
        def FuzzyMatchUDF(a, b):
            return fuzz.ratio(a, b)

        matches_df = matches_df.withColumn(
            "fuzzy_first_name_ratio",
            FuzzyMatchUDF(f.col(self.roster_map["first_name"]), f.col(data_map["first_name"])),
        ).withColumn(
            "fuzzy_last_name_ratio",
            FuzzyMatchUDF(f.col(self.roster_map["last_name"]), f.col(data_map["last_name"])),
        )

        thresh = 95
        matches_df = matches_df.filter(
            f"fuzzy_first_name_ratio >= {thresh} and fuzzy_last_name_ratio >= {thresh}"
        )
        return matches_df

    def r9(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 9 (Fuzzy 90 First Name, Fuzzy 90 Last Name, DOB, 2 Digit Lat/Long)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        join_conditions = [
            f.round(self.df[self.roster_map["lat"]], 2) == f.round(data_df[data_map["lat"]], 2),
            f.round(self.df[self.roster_map["long"]], 2) == f.round(data_df[data_map["long"]], 2),
        ]

        matches_df = self.roster_exact_join(data_df, data_map, join_conditions)

        @f.udf("int")
        def FuzzyMatchUDF(a, b):
            return fuzz.ratio(a, b)

        matches_df = matches_df.withColumn(
            "fuzzy_first_name_ratio",
            FuzzyMatchUDF(f.col(self.roster_map["first_name"]), f.col(data_map["first_name"])),
        ).withColumn(
            "fuzzy_last_name_ratio",
            FuzzyMatchUDF(f.col(self.roster_map["last_name"]), f.col(data_map["last_name"])),
        )

        thresh = 90
        matches_df = matches_df.filter(
            f"fuzzy_first_name_ratio >= {thresh} and fuzzy_last_name_ratio >= {thresh}"
        )
        return matches_df

    def r10(self, data_df: DataFrame, data_map: dict):
        """ Matching Rule 10 (Fuzzy 95 First Name, Fuzzy 95 Last Name, DOB)

        Args:
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """

        if not all([x in data_map.keys() for x in self._required_cols]):
            raise Exception(f"Ensure {self._required_cols} are all defined in data column map")

        join_conditions = [
            f.round(self.df[self.roster_map["lat"]], 2) == f.round(data_df[data_map["lat"]], 2),
            f.round(self.df[self.roster_map["long"]], 2) == f.round(data_df[data_map["long"]], 2),
        ]

        matches_df = self.roster_exact_join(data_df, data_map, join_conditions)

        @f.udf("int")
        def FuzzyMatchUDF(a, b):
            return fuzz.ratio(a, b)

        matches_df = matches_df.withColumn(
            "fuzzy_first_name_ratio",
            FuzzyMatchUDF(f.col(self.roster_map["first_name"]), f.col(data_map["first_name"])),
        ).withColumn(
            "fuzzy_last_name_ratio",
            FuzzyMatchUDF(f.col(self.roster_map["last_name"]), f.col(data_map["last_name"])),
        )

        thresh = 95
        matches_df = matches_df.filter(
            f"fuzzy_first_name_ratio >= {thresh} and fuzzy_last_name_ratio >= {thresh}"
        )
        return matches_df

    def match_on_rule(self, rule_num: str, data_df: DataFrame, data_map: dict):
        """ Call matching rule based on rule identifier

        Args:
            rule_num (str): Rule identifier
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns

        Returns:
            DataFrame: Potential Matches from roster to data df
        """
        matching_rule_method = f"r{rule_num}"
        if hasattr(self, matching_rule_method) and callable(getattr(self, matching_rule_method)):
            func = getattr(self, matching_rule_method)
            return func(data_df, data_map)

    def match(
        self, spark, sc, data_df: DataFrame, data_map: dict, rule_nums=[_ for _ in range(1, 11)],
    ):
        """ Matches roster to enriched data

        Args:
            spark (SparkSession): PySpark Instance
            sc (SparkContext): Spark Context
            data_df (DataFrame): Data DataFrame (Examples include Infutor and Acxiom)
            data_map (dict): Dictionary labeling required columns
            rule_nums (list, optional): Rule identifiers to use in matching

        Returns:
            DataFrame: Potential Matches and bitmask from individual rule matching results
        """

        # Create empty match table
        match_cols = [
            t.StructField(self.roster_map["id"], t.StringType(), True),
            t.StructField(data_map["id"], t.StringType(), True),
            t.StructField("is_likely_match", t.BooleanType(), True),
        ]
        rule_bit_cols = [t.StructField(f"r{i}", t.BooleanType(), True) for i in rule_nums]
        match_table_schema = t.StructType(match_cols + rule_bit_cols)
        match_table_df = spark.createDataFrame(sc.emptyRDD(), match_table_schema)

        # Generate matches for each rule
        for rule in rule_nums:
            match_df = self.match_on_rule(rule, data_df, data_map)
            match_table_df = match_table_df.unionByName(
                match_df.select([self.roster_map["id"], data_map["id"]]).withColumn(
                    f"r{rule}", f.lit(True)
                ),
                allowMissingColumns=True,
            )

        # Left join back to initial roster to preserve individuals without potential matches
        match_table_df = self.df.select(self.roster_map["id"]).join(
            match_table_df, self.roster_map["id"], "left"
        )

        # Collapse multiple matches into a single record with correct bitmask
        rule_aggregations = [f.max(f"r{rule}").alias(f"r{rule}") for rule in rule_nums]
        match_table_df = (
            match_table_df.groupBy([self.roster_map["id"], data_map["id"]])
            .agg(f.max("is_likely_match").alias("is_likely_match"), *rule_aggregations)
            .fillna(False)
        )

        # Find most likely matches
        w = Window.partitionBy(self.roster_map["id"])
        match_table_df = (
            match_table_df.fillna(False)
            .withColumn(
                "rule_matches",
                reduce(add, [f.col(f"r{i}").cast(t.IntegerType()) for i in rule_nums]),
            )
            .withColumn("max_rule_matches", f.max("rule_matches").over(w))
            .withColumn(
                "is_likely_match",
                f.when(
                    (
                        (f.col("rule_matches") == f.col("max_rule_matches"))
                        & (f.col(data_map["id"]).isNotNull())
                    ),
                    True,
                ).otherwise(False),
            )
            .drop("rule_matches", "max_rule_matches")
        )

        return match_table_df

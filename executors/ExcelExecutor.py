from executors.Executor import Executor
from helpers.DirectoryHelper import DirectoryHelper
from helpers.ExcelHelper import ExcelHelper
from helpers.FileHelper import FileHelper
from models.Action import Action
from models.Step import Step

class ExcelExecutor(Executor):
    _seplst = list("\n")

    def __init__(self):
        self.excelhelper = ExcelHelper()
        self.filehelper = FileHelper()
        self.directoryhelper = DirectoryHelper()

    def __initialize(self, step:Step, action:Action):
        self.wb = step.getOptions().get('workbook')
        self.sh = step.getOptions().get('sheet')
        self.sheet = self.__getSheet()
        self.pathbase = f'{step.path}/'
        self.path = action.get('path')
        self.src = action.get('src')
        self.module = step.module


    def execute(self, step:Step, action:Action):
        self.__initialize(step, action)
        operation = action.get('operation')
        self.__selectOperation(operation, action)

    def __selectOperation(self, operation:str, action:Action):
        if operation == "GetDataProcess":
            self.generateGetDataProcess(action)
        if operation == "PrepareDataProcess":
            self.generatePrepareDataProcess(action)
        if operation == "GenerateLocal":
            self.generateGenerateLocal(action)
        if operation == "GetDataProcessTest":
            self.generateGetDataProcessTest(action)
        if operation == "Parametry":
            self.generateParametry(action)

    def getInitialParametry(self, action):
        fromKey = action.get('sources_from')
        toKey = action.get('sources_to')
        colValues = action.get('inputfields_from')
        return self.excelhelper.convertColsToDict(self.sheet, fromKey, toKey, colValues)

    def getSourceJoin(self, action):
        fromKeyJoin = action.get('object_full_from')
        toKeyJoin = action.get('object_full_to')
        colValuesJoin = action.get('sources_full_to')
        return self.excelhelper.convertColsToDict(self.sheet, fromKeyJoin, toKeyJoin, colValuesJoin)

    def getOutputFields(self, action):
        fromKeyJoin = action.get('object_joins_from')
        toKeyJoin = action.get('object_joins_to')
        colValuesJoin = action.get('output_fields_from')
        return self.excelhelper.convertColsToDict(self.sheet, fromKeyJoin, toKeyJoin, colValuesJoin)

    def __createOutputFields(self, dict:{}):
        outputfieldslst = []
        for key in dict.keys():
            valuelst = dict.get(key).replace('\n', ',').split(',')
            cols = ", ".join(list(set(f"\"{i.strip()}\"" for i in valuelst)))
            outputfieldslst.append(f'\tval LIST_COLS_{key.upper()} = List({cols}).map(col)')
        return "\n".join(outputfieldslst)


    def generateParametry(self, action):
        inirialparametry = self.__createParametryAlias(self.getInitialParametry(action))
        sourcejoins = self.__createSourceJoin(self.getSourceJoin(action))
        outputfields = self.__createOutputFields(self.getOutputFields(action))
        self.__replaceValue(f'{inirialparametry}\n\n{sourcejoins}\n\n{outputfields}')

    def __createJoinAlias(self, value:str):
        return f'\tval ALIAS_{value.strip().upper()} = \"{value.lower()}\"'

    def __createSourceJoin(self, dict:{}):
        joinDict = {}
        for value in list(dict.values()):
            for opt in value.replace("\n", ",").split(","):
                joinDict.setdefault(opt, self.__createJoinAlias(opt))
        for key in dict.keys():
            joinDict.setdefault(key, self.__createJoinAlias(key))
        valueslst = joinDict.values()
        return "\n".join(valueslst)


    def __createParametryAlias(self, dict:{}):
        inputlst = []
        columnlst = self.__formatCollst(dict)
        for source in dict.keys():
            alias = source.strip().lower()
            alias_upper = alias.upper()
            inputlst.append(f"val INPUT_ROUTE_{alias_upper} = \"{self.module}.inputs.{alias}\"")
        parametrylst = (inputlst + self._seplst + columnlst)
        return "\n\t".join(parametrylst)

    def __formatCollst(self, dict):
        collst = []
        for key in dict.keys():
            fields = ",".join(list(map(self.__generateCollst, dict.get(key).split(','))))
            collst.append(f'val LIST_COLS_{key.strip().upper()} = List({fields}).map(col)')
        return collst

    def __generateCollst(self, value):
        valuelst:[] = value.strip().lower().replace("\n", ",").split(",")
        return ", ".join(list(set(f"\"{i.strip()}\"" for i in valuelst)))

    def generateGetDataProcessTest(self, action:Action):
        fromKey = action.get('sources_from')
        toKey = action.get('sources_to')
        colValues = action.get('inputfields_from')
        test = self.__createTest(self.excelhelper.convertColsToDict(self.sheet, fromKey, toKey, colValues))
        self.__replaceValue(f'{test}')

    def __formatTest(self, id, alias:str, columns):
        alias_capitalize = alias.capitalize()
        alias_upper = alias.upper()
        firstsentence = f"\t\"{id}. When read Persons and process get{alias_capitalize}\" should \"get a dataframe with ??? rows and {columns} columns\" in " + '{\n'
        secondsentence = f"\t\tval dfReturn = new GetDataProcess(spark, ConfigFactory.parseString(configString)).getInputs(ALIAS_{alias_upper})\n"
        firstassert = "\t\tassert(dfReturn.count() == Long.MaxValue)\n"
        secondassert = f"\t\tassert(dfReturn.columns.length == {columns})\n" + '\t}\n'
        return f"{firstsentence}{secondsentence}{firstassert}{secondassert}"

    def __createTest(self, dict:{}):
        test = []
        id = 1
        for testname in dict.keys():
            fields:str = dict.get(testname).replace("\n", ",").split(',')
            test.append(self.__formatTest(id, testname.strip(), len(fields)))
            id += 1
        return "\n".join(test)

    def __replaceValue(self, value:str):
        self.filehelper.replace_value(f'{self.pathbase}/{self.src}', 'input_replace', f'{value}')

    def generateGenerateLocal(self, action):
        values = self.__getValidValuesFromCells(action.get('object_joins_from'), action.get('object_joins_to'))
        generateconditions = list(map(self.__createConditions, values))
        conditions = "\n".join(generateconditions)
        generatePatternMatch = list(map(self.__createPatternMatch, values))
        patternmatch = self.__createFunctionPatternMatch("\n".join(generatePatternMatch))
        fromKey = action.get('object_joins_from')
        toKey = action.get('object_joins_to')
        colValues = action.get('sources_from')
        generatejoins = self.__createJoins(self.excelhelper.convertColsToDict(self.sheet, fromKey, toKey, colValues))
        joins = "\n".join(generatejoins)
        self.__replaceValue(f'{conditions}\r\n{joins}\n{patternmatch}')

    def __createJoins(self, dict:{}):
        # val joinSgto = JoinTable(ALIAS_JOIN_BC_VRF, FIL_022, conditionCustomer, PARAM_LEFT_JOIN, LIST_COLS_SGTO)
        joins = []
        for joinname in dict.keys():
            alias = joinname.upper()
            alias_capilize = joinname.capitalize()
            alias_lower = joinname.lower()
            valuelst = dict.get(joinname).upper().replace("\n", ",").split(",")
            cols = ", ".join(list(set(f'ALIAS_{i}' for i in valuelst)))
            joins.append(f'\tval {alias_lower} = JoinTable({cols}, condition{alias_capilize}, ???, LIST_COLS_{alias})')
        return joins

    def __createPatternMatch(self, value:str):
        # case ALIAS_JOIN_SGTO => applyJoin(joinSgto)
        alias_lower = value.lower()
        alias = value.upper()
        return f'\t\tcase ALIAS_{alias} => applyJoin({alias_lower})'

    def __createConditions(self, value:str):
        # val conditionCustomer = col(COL_CONDITION_LEFT_CUSTOMER_ID) === col(COL_CONDITION_RIGHT_CUSTOMER_ID)
        alias_capitalize = value.capitalize()
        return f'\tval condition{alias_capitalize} = ???'

    def generatePrepareDataProcess(self, action: Action):
        values = self.__getValidValuesFromCells(action.get('object_transformation_from'), action.get('object_transformation_to'))
        generatealias = list(map(self.__createFilters, values))
        filterMap = self.__generateFilterMap(",\n".join(generatealias))
        generatefunctions = list(map(self.__createFunctions, values))
        filterFunctions = ("\n".join(generatefunctions))
        self.__replaceValue(f'{filterMap}{filterFunctions}')

    def __getSheet(self):
        wb = self.excelhelper.getWorkBook(self.wb)
        return self.excelhelper.getSheet(wb, self.sh)

    def __createFunctions(self, value:str):
        #def filRv09(dfHdarv009: DataFrame) : DataFrame = {
        #   dfHdarv009
        #}
        alias_capitalize = value.capitalize()
        return f'\n\tdef get{alias_capitalize}(df{alias_capitalize}:DataFrame):DataFrame = ' + '{\n\t' + f'\t\tdf{alias_capitalize}\n' + '\t}'

    def __getValidValuesFromCells(self, fromCell:str, toCell:str):
        invalidvalues = ['union', 'aggregates', 'object', 'filter']
        lstinvalidvalues = invalidvalues + list(set(i.upper() for i in invalidvalues)) + list(set(i.capitalize() for i in invalidvalues))
        values = self.excelhelper.getRowsRange(self.sheet, fromCell, toCell)
        for invalidvalue in lstinvalidvalues:
            values = list(filter((invalidvalue).__ne__, values))
        return values

    def __createFilters(self, value:str):
        # FIL_VEC -> sources(ALIAS_HDAUGVEC)
        alias = value.upper()
        alias_capitalize = value.capitalize()
        return f'\t\tALIAS_{alias} -> get{alias_capitalize}(sources(ALIAS_{alias}))'

    def __generateFilterMap(self, value):
        return "\ndef getFilters(sources: Map[String, DataFrame]):Map[String, DataFrame] = " + "{\n" + f"\tMap ( \n{value})" + "\n\t}\n"

    def generateGetDataProcess(self, action:Action):
        configpath = action.get('configpath')
        values = self.__getValidValuesFromCells(action.get('sources_from'), action.get('sources_to'))
        generatealias = list(map(self.__createMapAlias, values))
        self.__createDirectories(values)
        self.__writeConfig(values, configpath)
        self.__replaceValue(",\n".join(generatealias))

    def __writeConfig(self, values, configfilespath:str):
        for configfile in configfilespath.split(','):
            configvalue = self.__createConfig(values)
            self.filehelper.replace_value(f'{self.pathbase}/{configfile}', 'input_replace', configvalue)

    def __createConfig(self, values):
        configkeys = []
        for value in values:
            configkeys.append(f'{value}' + '{\n\t\t' + "type = \"avro\"\n\t\t" + "paths = [\n\t\t\t" +"\"your path here\"" + "\n\t\t]\n\t\t" + "applyConversions = false\n\t" + "}")
        return "\n\t".join(configkeys)

    def __createMapAlias(self, value:str):
        # (ALIAS_HDAUGVEC -> getDataFrame(INPUT_ROUTE_HDAUGVEC, LIST_COLS_HDAUGVEC))
        alias = value.upper()
        return f'\t\t\t\t\t(ALIAS_{alias} -> getDataFrame(INPUT_ROUTE_{alias}, LIST_COLS_{alias}))'

    def __createFunctionPatternMatch(self, value:str):
        return f'\n\tdef getDataFramesByKey(key:String):DataFrame = key match ' +  '{\n' + f'{value}' + '\n\t\tcase _ => inputs(key)\n' + '\t}'

    def __createDirectories(self, values):
        for directory in values:
            self.directoryhelper.create(f'{self.pathbase}/{self.path}/{directory}')
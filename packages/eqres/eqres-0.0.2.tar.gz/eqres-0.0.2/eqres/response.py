from datetime import datetime
from eqres.error_code import CODE_SYS
from json import dumps as json_dumps
from json import loads as json_loads
import traceback


class SetResponse:
    def __init__(self, code_sys=None):
        if code_sys is not None and type(code_sys) == dict:
            try:
                CODE_SYS.update(code_sys)
            except Exception as e:
                print(e, traceback.format_exc())
        self.code_sys = CODE_SYS
        self.start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.response_info = self.code_sys['init']

    def success(self, data, trans=0):
        """
        成功返回
        :param data: 数据体
        :param trans: 默认不需要数据转换
        :return: 统一处理函数
        """
        return self.res('success', data, trans)

    def warning(self, data, trans=0):
        """
        警告返回
        :param data: 数据体
        :param trans: 默认不需要数据转换
        :return: 统一处理函数
        """
        return self.res('warning', data, trans)

    def error(self, data, trans=0):
        """
        错误返回
        :param data: 数据体
        :param trans: 默认不需要数据转换
        :return: 统一处理函数
        """
        return self.res('error', data, trans)

    def info(self, data, msg=None, trans=0):
        """
        错误返回
        :param msg: 消息code
        :param data: 数据体
        :param trans: 默认不需要数据转换
        :return: 统一处理函数
        """
        if msg is None or isinstance(msg, dict) is False:
            msg = self.code_sys['unknown']
        self.response_info = msg
        self.data_fill(data, trans)
        return self.response_info

    def res(self, code, data, trans=0):
        """
        返回数据处理
        :param code: 编码
        :param data: 数据
        :param trans: 0-不做处理，1-字典转字符串，2-字符串转字典
        :return: 数据转换结果
        """
        self.response_info = self.code_sys[code]
        self.data_fill(data, trans)
        return self.response_info

    def data_fill(self, data, trans):
        """
        数据填充
        :param data: 数据体
        :param trans: 数据转换标识
        """
        if trans == 1:
            self.data_dumps(data)
        elif trans == 2:
            self.data_loads(data)
        else:
            self.response_info['data'] = data
        self.response_info['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.response_info['start_time'] = self.start_time

    def data_dumps(self, data):
        """
        字典转字符串
        :param data: 数据体
        """
        if isinstance(data, dict) or isinstance(data, list) or isinstance(data, tuple):
            try:
                data = json_dumps(data)
            except Exception as e:
                print('[eqres] [data_dumps]', str(e))
        self.response_info['data'] = data

    def data_loads(self, data):
        """
        字符串转字典
        :param data: 数据体
        """
        try:
            data = json_loads(data)
        except Exception as e:
            print('[eqres] [data_loads]', str(e))
        self.response_info['data'] = data

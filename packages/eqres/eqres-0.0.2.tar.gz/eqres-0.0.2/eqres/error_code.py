"""
全局返回码
"""

CODE_SYS = {
    'init': {
        'code': 0000,
        'message': 'default'
    },

    'unknown': {
        'code': 9999,
        'message': '未知原因'
    },

    'success': {
        'code': 1000,
        'message': '操作成功'
    },

    'warning': {
        'code': 5000,
        'message': '系统繁忙，请稍后'
    },

    'error': {
        'code': 4000,
        'message': '交易失败'
    },

    'wrong': {
        'code': 9000,
        'message': '系统异常'
    }
}

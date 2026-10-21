from db import query, execute


def list_rows(sql, params=()):
    return query(sql, params)


def save(sql, params=()):
    return execute(sql, params)

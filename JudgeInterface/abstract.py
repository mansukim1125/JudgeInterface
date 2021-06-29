from typing import Dict, List
from .lib.placeholder import Placeholder


class AbstractInterface:
    """
    AbstractInterface를 상속받아 새 DB Model의 Interface를 만들 수 있습니다. 새 Interface에서 다음의 변수를 사용하십시오:
    1. create_fields
        INSERT할 때 필수적으로 필요한 Fields를 List로 정의할 수 있습니다.
    2. retrieve_fields
        SELECT할 때 필요한 Fields를 List로 정의할 수 있습니다.
    3. update_fields
        UPDATE할 때 필수적으로 필요한 Fields를 List로 정의할 수 있습니다.
    4. table_name
        액세스할 테이블의 이름을 str로 정의할 수 있습니다.
    """
    def __init__(self, cur):
        """
        cur은 DB Connector의 cursor입니다. 이를 이용해 DB에 접근합니다.
        """
        self.cur = cur

    def perform_create(self, return_type=None, **data: Dict):
        """data를 table_name 테이블에 추가합니다."""
        keys_set = set(data.keys())
        unknown_fields = keys_set - set(self.create_fields)
        if len(unknown_fields) > 0:
            # TODO: 허용되지 않은 fields 출력.
            raise AttributeError(f'{str(unknown_fields)} field(s) is(are) not allowed')

        keys_list = list(data.keys())

        query_fields = ', '.join(keys_list)
        fields_values = tuple(data.get(key) for key in keys_list) # self.create_fields를 valid_fields로 바꿔도 무방.

        self.cur.execute(
            f'''
            INSERT INTO
            {self.table_name}({query_fields})
            VALUES({Placeholder.for_create_query(len(fields_values))})
            '''
            , fields_values
        )

        context = {key: data.get(key) for key in self.retrieve_fields} # self.create_fields를 self.retrieve_fields로 변경.
        context['id'] = self.cur.lastrowid
        if return_type != None:
            return return_type(**context)
        return context

    def perform_retrieve(self, return_type=None, project_fields: List = [], **where_kwargs: Dict):
        """table_name 테이블에서 project_fields Field를 where_kwargs의 조건으로 가져옵니다."""
        # project_fields중 self.retrieve_fields에 없는 fields가 있다면 AttributeError.
        unknown_fields = set(project_fields) - set(self.retrieve_fields)
        if len(unknown_fields) > 0:
            raise AttributeError(f'{str(unknown_fields)} field(s) is(are) not allowed')
        
        # len(project_fields) <= 0 이면 project_fields = self.retrieve_fields.
        if len(project_fields) <= 0:
            project_fields = self.retrieve_fields
        
        # where_kwargs.keys()중 self.retrieve_fields에 없는 fields가 있다면 AttributeError.
        unknown_where_fields = set(where_kwargs.keys()) - set(self.retrieve_fields)
        if len(unknown_where_fields) > 0:
            raise AttributeError(f'{str(unknown_where_fields)} field(s) is(are) not allowed')
        
        # project_fields placeholder 만들기. (공통)
        project_placeholder = Placeholder.for_select_query(project_fields)
        
        # where 없는 상태로 query문 만들기.
        query = f"""SELECT {project_placeholder}\nFROM {self.table_name}"""

        where_keys = list(where_kwargs.keys())
        # len(where_kwargs.keys()) <= 0 이면 where 절 없음.
        if len(where_keys) > 0:
            # where 있음.
            # where_kwargs placeholder 만들기.
            where_placeholder = Placeholder.for_where_query(where_keys)
            query += f'\nWHERE {where_placeholder}'
            where_values = tuple(where_kwargs.get(key) for key in where_keys)
            # query문 만들고 실행. (공통)
            self.cur.execute(query, where_values)
        else:
            self.cur.execute(query)

        # fetchall / many하고 for loop에서 self.DTO의 instance로 구성된 List를 반환. (공통)
        lst = []
        if return_type != None:
            for t in self.cur:
                instance = return_type(**t)
                lst.append(instance)
        else:
            for t in self.cur:
                lst.append(t)

        return lst

    def perform_update(self, id: int, **data: Dict) -> Dict:
        """id로 지정되는 한 튜플을 data로 갱신합니다."""
        keys_set = set(data.keys())
        unknown_fields = keys_set - set(self.update_fields)
        if len(unknown_fields) > 0:
            raise AttributeError(f'{str(unknown_fields)} field(s) is(are) not allowed')

        if len(keys_set) <= 0: return None# 허용된 fields에 해당하는 data가 없으면 update할 data가 없다는 것을 의미하므로 종료.

        keys_list = list(data.keys())
        fields_values = tuple(data.get(key) for key in keys_list)
        
        self.cur.execute(
            f'''
            UPDATE {self.table_name}
            SET {Placeholder.for_update_query(keys_list)}
            WHERE id = ?
            ''',
            (*fields_values, id)
        )
        returnable_fields = list(set(self.retrieve_fields).intersection(keys_set))

        context = {key: data.get(key) for key in returnable_fields}

        return context

    def perform_delete(self, id: int) -> None:
        """id로 지정되는 한 튜플을 삭제합니다."""
        self.cur.execute(
            f'''
            DELETE FROM {self.table_name}
            WHERE id = ?
            ''',
            (id,)
        )
        return None

    def create(self, return_type=None, **data: Dict):
        """
        data를 self.table_name 테이블에 추가합니다. perform_create(self, **data)와 다른 점이라면 오버라이드하여 data의 특정 field를 가공할 수 있습니다.
        """
        return self.perform_create(return_type, **data)

    def retrieve(self, return_type=None, project_fields: List = [], **where_kwargs: Dict):
        """
        table_name 테이블에서 project_fields Field를 where_kwargs의 조건으로 가져옵니다.
        """
        return self.perform_retrieve(return_type, project_fields, **where_kwargs)

    def update(self, id: int, **data: Dict) -> Dict:
        """
        id로 지정되는 한 튜플을 data로 갱신합니다. perform_update(self, id, **data)와 다른 점이라면 오버라이드하여 data의 특정 field를 가공할 수 있습니다.
        """
        return self.perform_update(id, **data)

    def delete(self, id: int) -> None:
        """
        id로 지정되는 한 튜플을 삭제합니다.
        """
        return self.perform_delete(id)

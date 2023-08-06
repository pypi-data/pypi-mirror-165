(function(){"use strict";var n={beginPayload:!0,testReport:[{test:{title:"HARDCODED: Identity function should return the same object",function:`def identity(x):
    return x
`,input:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`,expected_output:`Unnamed: 0,useful col
1,1
2,2
3,4
3,3
`},result:{successful:!1,status:"WrongResult",testrun_output:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`,assertion_error_message:`DataFrame.iloc[:, 0] (column name="Unnamed: 0") are different

DataFrame.iloc[:, 0] (column name="Unnamed: 0") values are different (25.0 %)
[index]: [0, 1, 2, 3]
[left]:  [1, 2, 3, 3]
[right]: [1, 2, 3, 4]`}},{test:{title:"HARDCODED: Drop Unnamed should drop the column 'Unnamed: 0'",function:`def drop_unnamed(df):
    return df.drop(columns=['Unnamed: 0'])
`,input:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`,expected_output:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`},result:{successful:!1,status:"WrongResult",testrun_output:`useful col
1
2
4
3
`,assertion_error_message:`DataFrame are different

DataFrame shape mismatch
[left]:  (4, 2)
[right]: (4, 1)`}},{test:{title:"HARDCODED: Drop Unnamed v2 should drop the column 'Unnamed: 0'",function:`def drop_unnamed2(df):
    return df.drop(columns=['Unnamed: 0'])
`,input:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`,expected_output:`0
"[1, 2, 4, 3]"
`},result:{successful:!1,status:"Crash",traceback:`Traceback (most recent call last):
  File "/home/remiconn/battleground/env/lib/python3.10/site-packages/presyence/simpletests.py", line 49, in run
    assert_same = pd.testing.assert_serie_equal
AttributeError: module 'pandas.testing' has no attribute 'assert_serie_equal'
`}},{test:{title:"HARDCODED: Drop Unnamed should drop the column 'Unnamed: 0'",function:`def drop_unnamed5(df):
    return drop_unnamed3(df.yolo)
`,input:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`,expected_output:`useful col
1
2
4
3
`},result:{successful:!1,status:"Crash",traceback:`Traceback (most recent call last):
  File "/home/remiconn/battleground/env/lib/python3.10/site-packages/presyence/simpletests.py", line 45, in run
    testrun_output = self.function(self.input)
  File "/home/remiconn/battleground/experience_zone/realcode.py", line 14, in drop_unnamed5
    return drop_unnamed3(df.yolo)
  File "/home/remiconn/battleground/env/lib/python3.10/site-packages/pandas/core/generic.py", line 5575, in __getattr__
    return object.__getattribute__(self, name)
AttributeError: 'DataFrame' object has no attribute 'yolo'
`}},{test:{title:"HARDCODED: Identity function should return the same object",function:`def identity(x):
    return x
`,input:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`,expected_output:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`},result:{successful:!0,status:"Success"}},{test:{title:"HARDCODED: Drop Unnamed should drop the column 'Unnamed: 0'",function:`def drop_unnamed(df):
    return df.drop(columns=['Unnamed: 0'])
`,input:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`,expected_output:`useful col
1
2
4
3
`},result:{successful:!0,status:"Success"}},{test:{title:"HARDCODED: Drop Unnamed v2 should drop the column 'Unnamed: 0'",function:`def drop_unnamed2(df):
    return df.drop(columns=['Unnamed: 0'])
`,input:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`,expected_output:`useful col
1
2
4
3
`},result:{successful:!0,status:"Success"}},{test:{title:"HARDCODED: Drop Unnamed v4 should drop the column 'Unnamed: 0'",function:`def drop_unnamed4(df):
    return drop_unnamed3(df)
`,input:`Unnamed: 0,useful col
1,1
2,2
3,4
4,3
`,expected_output:`useful col
1
2
4
3
`},result:{successful:!0,status:"Success"}}],endPayload:!0};self.postMessage("Hello from the worker");const e=n.testReport;console.log("Worker is executed"),self.onmessage=()=>{self.postMessage(e)}})();

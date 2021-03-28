from typing import Dict, List, Tuple, Union

ApiResponse = Tuple[str, int]

LoginJSON = Dict[
    str,
    Union[
        str,
        Dict[str, Union[str, int]],
    ],
]

MemberJSON = Dict[
    str,
    Union[
        int,
        str,
        bool,
        List[str],
    ],
]

TokenJSON = Dict[str, Union[int, str, bool]]

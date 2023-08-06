from lupo import *

window = Window()
window.set_size(256, 256)

window.body = View(children=[
    Column(style=Style(gap=px(10)), children=[

        Row(style=Style(gap=px(10)), children=[
            Button("Test 1", Style(width=px(100), height=px(100))),
            Button("Test 2", Style(width=px(100), height=px(100))),
        ]),

        Row(style=Style(gap=px(10)), children=[
            Button("Test 3", Style(width=px(100), height=px(100))),
            Button("Test 4", Style(width=px(100), height=px(100))),
        ]),

    ])
])

window.open()

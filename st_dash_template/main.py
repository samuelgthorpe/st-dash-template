"""
Main entry to run primary st_dash_template experiment.

# NOTES
# ----------------------------------------------------------------------------|


Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
from resources.app import data, openai_client
from types import ModuleType
from markdown_strings import code_block
from datetime import datetime
import plotly
import pandas  # noqa
import numpy  # noqa
import scipy  # noqa
import stats  # noqa
import statsmodels  # noqa
from dash import (
    Dash,
    html,
    dash_table,
    Input,
    Output,
    State,
    callback,
    dcc)


# # Imports
# -----------------------------------------------------|
DOWNLOAD_DIR = '/home/sam/Downloads'
GPT_MODEL = "gpt-3.5-turbo"


# # Helper Methods
# -----------------------------------------------------|
def build_layout():
    """Build the app layout."""
    return [
        html.Div(
            style={
                "position": "relative",  # Positioning context for the icon
                "padding": "10px",
                "border-bottom": "1px solid #ddd",
                "background-color": "#f9f9f9",
            },
            children=[
                html.H2(
                    f' {data["meta"]["name"]} Dataset Explorer',
                    style={"display": "inline-block"}
                    ),
                html.Img(
                    src="https://static.wixstatic.com/media/d90f6c_291394c77a384baf8b4b8641f42b5cdf~mv2.jpg/v1/fill/w_442,h_482,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/ThorpeHeadshot_WebSize.jpg",
                    style={"position": "absolute", "right": "1%", "height": "52px", "width": "52px", "border-radius": "50%"},
                )
            ]
        ),
        dcc.Markdown(f'''
            {data['desc']['header']}
            '''),
        dash_table.DataTable(
            data=data['dfr'].to_dict('records'),
            page_size=5,
            style_header={
                'color': '#333333',
                'fontWeight': 'bold'
                 },
            ),
        html.Div([
            html.Div(
                'Input Command',
                style={'whiteSpace': 'pre-line'}
                ),
            dcc.Textarea(
                id='textarea-input',
                style={'width': '99%', 'height': 30},
                ),
            html.Button(
                'Submit',
                id='textarea-submit-button',
                n_clicks=0),
            html.Div(
                id='textarea-output',
                style={'whiteSpace': 'pre-line'}
                )
            ])
    ]


@callback(
    Output('textarea-output', 'children'),
    Input('textarea-submit-button', 'n_clicks'),
    State('textarea-input', 'value')
)
def update_output(n_clicks, value):
    """Update the html output div."""
    if n_clicks > 0:
        prompt, flag = build_prompt_from_user_input(value)
        response = get_completion(prompt)
        children = handle_response(response, flag)
        return children


def build_prompt_from_user_input(value):
    """Build the OpenAi prompt."""
    if value and value[:5] == "chat:":
        prompt = f'{data["desc"]['prompt']}\n {data["chat_prompt"]}\n {value}'
        flag = 'chat'
    else:
        prompt = f'{data["desc"]['prompt']}\n {data["cmd_prompt"]}\n {value}'
        flag = 'cmd'

    return prompt, flag


def get_completion(prompt):
    """Call to OpenAi API to get completion."""
    completion = openai_client.chat.completions.create(
        model=GPT_MODEL,
        messages=[{"role": "user", "content": prompt}]
        )
    response = completion.choices[0].message.content
    return response


def handle_response(response, flag):
    """Based on the completion content, build html children."""
    if flag == 'cmd':
        response = munge_validate_response(response)
        evaluated = evaluate_response(response)
        children = [
            dcc.Markdown(
                code_block(response, 'python'),
                dangerously_allow_html=True,
                style={"overflow-x": "scroll"}
            ),
            dcc.Store(id="text-store", data=response),
            html.Button(
                'Download',
                id='code-download-button',
                n_clicks=0),
            html.Div(
                id="file-message",
                style={"margin-top": "5px", "font-size": 11}
                ),
        ]

        if isinstance(evaluated, plotly.graph_objects.Figure):
            children.append(
                dcc.Graph(figure=evaluated)
                )
        else:
            children.append(
                dcc.Markdown(
                    f'Evaluated Response: \n{evaluated}',
                    dangerously_allow_html=True,
                    style={"overflow-x": "scroll"}
                    )
                )
    elif flag == 'chat':
        children = [
            dcc.Markdown(
                f'Chat Response: \n\n{response}',
                dangerously_allow_html=True,
                style={"overflow-x": "scroll"}
                )
        ]

    return children


def evaluate_response(response):
    """Evaluate the reponse as code and return output."""
    try:
        compiled = compile(response, 'multistring', 'exec')
        module = ModuleType("testmodule")
        exec(compiled, module.__dict__)
        return module.response_function(data['dfr'])
    except Exception as err:
        return err.__str__()


def munge_validate_response(response):
    """Munge response for now. Eventually validate."""
    def_idx = response.find("def")
    if def_idx > 0:
        response = response[def_idx:]

    return_idx = response.find("return")
    last_line = response[return_idx:]
    last_line_split = last_line.split('\n')
    if len(last_line_split) > 1:
        response = response[:return_idx] + last_line_split[0]

    return response


@callback(
    Output("file-message", "children"),
    Input('code-download-button', 'n_clicks'),
    State('text-store', 'data'),
    prevent_initial_call=True
)
def download_code(n_clicks, code):
    """Download the code Python block."""
    if n_clicks > 0:
        tag = '_'.join(data["meta"]["name"].split())
        file_path = f'{DOWNLOAD_DIR}/{tag}_method_{_now()}.py'
        with open(file_path, "w") as file:
            file.write(code)

        return f"File saved to: {file_path}"


def _now():
    """Return string with current datetime."""
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%dT%H:%M:%S")
    return now_str


# # Main Method
# -----------------------------------------------------|
def main():
    """Run main method."""
    app = Dash(__name__, suppress_callback_exceptions=True)
    app.layout = build_layout()
    app.run(debug=True)


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":  # pragma: no cover
    main()

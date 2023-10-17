example_dict = {"nodes":[{"name":"B","outputs":{},"isInitialState":False},{"name":"A","outputs":{},"isInitialState":True},{"name":"D","outputs":{},"isInitialState":False},{"name":"C","outputs":{},"isInitialState":False}],"links":[{"name":"e1","source":"A","dest":"B"},{"name":"e2","source":"A","dest":"C"},{"name":"e3","source":"C","dest":"D"},{"name":"e5","source":"D","dest":"A"},{"name":"e4","source":"D","dest":"B"},{"name":"e6","source":"B","dest":"A"}]}
verilog_code = ""

def parse():
    # TODO get input json and parse the output
    pass

def to_verilog(input_fsm):
    body = get_body(input_fsm=input_fsm)
    registers = [node["name"] for node in input_fsm["nodes"]]
    registers = str(",".join(map(str, registers)))
    events    = [event["name"] for event in input_fsm["links"]]
    events = str(",".join(map(str, events)))
    base_code = \
f"""
module FSM(
    Reset,clk,
    {registers},
    {events}
);
input Reset,clk;
input {events};
output reg {registers};
{body}

endmodule
"""
    return base_code


def get_body(input_fsm) : 
    
    assignments_code = ""
    initial_code = ""
    for node in input_fsm["nodes"]:

        node_name = node["name"]
        if node["isInitialState"] : 
            initial_code += f"\t{node_name} <= 1;\n"
        else : 
            initial_code += f"\t{node_name} <= 0;\n"
        node_state_line = f"\t{node_name} <= "
        for link in input_fsm["links"] : 
            if node["name"] == link["dest"] :
                source = link["source"]
                event = link["name"]
                # print(node["name"], source,event)
                node_state_line += f"{source}&{event} | "
        node_state_line = f"{node_state_line[:-2]};\n"
        # print("line---->",node_state_line)
        assignments_code += node_state_line
    body_code = \
        f"""
always @(posedge clk) begin\n
if(~Reset) begin

{initial_code}
end
else begin

{assignments_code}
end

end
        """
    return body_code


if __name__ == "__main__":
    print(to_verilog(input_fsm=example_dict))


module FSM(
    Reset,clk,
    B,A,D,C,
    e1,e2,e3,e5,e4,e6
);
input Reset,clk;
input e1,e2,e3,e5,e4,e6;
output reg B,A,D,C;

always @(posedge clk) begin

if(~Reset) begin

	B <= 0;
	A <= 1;
	D <= 0;
	C <= 0;

end
else begin

	B <= A&e1 | D&e4 ;
	A <= D&e5 | B&e6 ;
	D <= C&e3 ;
	C <= A&e2 ;

end

end
        

endmodule

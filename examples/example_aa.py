import string_recorder


rec = string_recorder.StringRecorder()

frames = [

"""
      ◯◯◯◯ 
      ◯ ･ω･ ◯  がおー 
        ◯◯◯ 
    .c(,_ｕｕﾉ 
""",
"""
                         ◯。    ◯ 
        ミﾊｯｸｼｭ      ◯        ｏ      ◯ 
       ミ  ｀д´∵°  。  ｏ  ◯ 
    .c(,_ｕｕﾉ   ◯  ◯      ◯ 
""",
"""
 
        ∧∧       
       ( ･ω･)           .◯◯◯  ◯◯◯ 
    .c(,_ｕｕﾉ     ..◯◯  ◯◯◯    .◯◯◯  ◯◯ 
"""
]

for frame in frames:
    rec.record_frame(frame)
rec.make_gif('aa1.gif', speed=2.0)

frames = [
"""         ∧__,,∧ 
         ( ´･ω･)    これが有名な”お断りちゃんのお面”か・・・ﾄﾞｷﾄﾞｷ 
        /Ｏ（ ﾟωﾟ )Ｏ 
        し―-J """,
"""         ∧__,,∧ 
         (-（ ﾟωﾟ )    ﾑｽﾞﾑｽﾞ････ 
    ((  /  つ  Ｏ )) 
        し―-J""",
"""          ∧__,,∧ 
         ∩-（ ﾟωﾟ )  お断りします・・・あっ、やっぱり言っちゃった 
        /      ﾉ 
        し―-J""",
"""           ﾊ,,ﾊ 
         (=（ ﾟωﾟ )    お、お、おこと･･･ 
    ((  /  つ  Ｏ ))   や、やばい！ 
        し―-J""",
"""           ﾊ,,ﾊ 
         ( ﾟωﾟ )    ふぅ・・・  危なかった・・・  外れなくなるのお断りします。 
        /Ｏ( ´･ω･)Ｏ 
        し―-J"""]

for frame in frames:
    rec.record_frame(frame)
rec.make_gif('aa2.gif', speed=2.0)

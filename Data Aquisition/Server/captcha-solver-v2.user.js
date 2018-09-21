// ==UserScript==
// @name         Captcha-Solve-V2
// @author       ECHibiki - /qa/
// @description  solves captchas sending images to a localhost server.
// @version      1.0
// @namespace    http://datasets.verniy.xyz/
// @include		 https://www.google.com/recaptcha/api/fallback*
// @include      http://boards.4chan.org/*
// @include      https://boards.4chan.org/*
// @grant        GM_xmlhttpRequest
// @run-at document-end
// @icon  data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/4QB4RXhpZgAATU0AKgAAAAgABgExAAIAAAARAAAAVgMBAAUAAAABAAAAaAMDAAEAAAABAAAAAFEQAAEAAAABAQAAAFERAAQAAAABAAAOxFESAAQAAAABAAAOxAAAAABBZG9iZSBJbWFnZVJlYWR5AAAAAYagAACxj//bAEMAAgEBAgEBAgICAgICAgIDBQMDAwMDBgQEAwUHBgcHBwYHBwgJCwkICAoIBwcKDQoKCwwMDAwHCQ4PDQwOCwwMDP/bAEMBAgICAwMDBgMDBgwIBwgMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDP/AABEIAHQAeAMBIgACEQEDEQH/xAAfAAABBQEBAQEBAQAAAAAAAAAAAQIDBAUGBwgJCgv/xAC1EAACAQMDAgQDBQUEBAAAAX0BAgMABBEFEiExQQYTUWEHInEUMoGRoQgjQrHBFVLR8CQzYnKCCQoWFxgZGiUmJygpKjQ1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4eLj5OXm5+jp6vHy8/T19vf4+fr/xAAfAQADAQEBAQEBAQEBAAAAAAAAAQIDBAUGBwgJCgv/xAC1EQACAQIEBAMEBwUEBAABAncAAQIDEQQFITEGEkFRB2FxEyIygQgUQpGhscEJIzNS8BVictEKFiQ04SXxFxgZGiYnKCkqNTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqCg4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2dri4+Tl5ufo6ery8/T19vf4+fr/2gAMAwEAAhEDEQA/APozxLp8ujX7W89pLZ3EbEPHIpVgckdKqxz+XEVb5Wz15z9MVqeOvHd98R/GF5rl5sW8vsbxCu1VAXYABnpgY5PNY8SZHRiM9f8APvXsGZcubX7PpFrKl1DL9s374Y5MyRbSB86Y4z1HJz7YqraRrJdfvP8AVnuO1aCeFtSjsv7QazvItPiuEt5LryiscUjDIUt0BxzyelZMrCCNSqyTSbgojQfM7EhVVeeSSQO3X05o2Dc6PS/C1xcTwXGLuztVLF7uEYO1flKxMQVMhJCgnIXJYhgu1t+xtQLOOzt44tPsFcukKbmVWxjezHLySEYBkcs57nGAI9C0WXSNBt7a4l8yZcvKUJ2tI2N2PYABQepCLnmu++Hvw9k1K6+0TSbbWPjchI83I6Dvgg9+x968uriFJ+Rs8O1oyh4N+HE2sSLIy/uR1PTNel6f4RsdNt1VYwy7RnPr3/CtC3ijtbfyokWONeFCjCrQh3nHfrkc5rjlNs6IxSRpeELlNNvWt/Mgs7W8UxTyeQGEanuAP8815f8AFj9nSz+ImoSXGg6hb+H9caYbbw23m2l5yADNCGQkkc70ZHzgsXA2nvmJSTG5frTTyM+p/WiFSUHeISinueZ/EeD4xfCr7Po66mmqWclvkS2lxEr5BxyZVTAPYby3qO9eJ69Za1FdT3GsWOsWsxO6ee7t3CKf9qXBj/JiK+v7tdltGJGhm+0J5hIbcyjJXY3p0zj3FQTaYBDD5sK+TIu6POD8uSOPTkH06V1Rx009UjL6vG2h8fQXLQRLNbzbvMUjKH+Fhg8+hBPTqDUBn83y9qIu3cdwbDP35JOOO2AM+5r0f9ovwDD4X8UWt9Zr5drqyNuQfdSaPbk+nzKwPuVY9ck+eTEKobq33eR7Yr0qdRTipIwlGzsTIy3ARfLjjX+NlUtgdyR7Dnj0op2p6jFqgtRBZw2f2e3WKTa7N9odckyHPc+g44FFaEk0+nwxW8Xl3CzNINzgKQYzzwcjB6A5HrUIRBhfMWPzMgsxPyY+mev0/rWleWMUNo0igbupCnAH+fSsu+/0yTdI0kk7EIEUbpJCBjAHU4A/ADtRcB15fbbZbeO4mELnfJGJS0ZYcBseuAeozj614/8AHKy8Q+P9WsbbRbqzsdL0m7MzT3WoX2kx3lwqFY57bVbQlIdm6RF81XjkaQkgqqPX1N+z18E4/Eeqz3XivTt2m+Vi3gl+aGQn/nof4xj+FcrzjLda9ST4bWdnqErxTNHb7z5ccI2hF7DJ7e2OleXja8Zw9nHruehgJSo1VWtqtrn58w/Gf4x/Bi3Ua9D4mislHyTeLPDv9u6aqdQ39saHljkfxT2gPc57fUHwV/bij8UeDtKX/hHLPXZGt42dvB/iOy1h9zAE/wCiytb3YGT0MWe3XivXpPhR4bjeSRNPa1uJBgy2dxJZyPzn5mhZC3frnrXP+MP2dPD/AI/h8rVoYdYVRiMarp1lqDRgdvNkgM+O2fN3e4ryXTmlaEvv/p/ket9dw1SV61Ja9Vpb0Stf5th/w194EW5jt9ZvNS8I3QdYWt/EOkXmkszHOMvNGIyTg/dYjiu08E+O9B+IP/ID17RdaUZOdOvorzAHX/VseleD+OvgLafBPw899a+JbTwppszeWIrfxXfeG7d+4VRcS3tvI3HCCFQa+fdW1nw74x1SaFtP1C4aFdyanrPgDRr23Z+w+0RzadfPg4y3lgHsfQjHEb8t/T/g/wCQnSy+fw1HH1V/wS/U+ivGPxR8beFfiZdWfxMk8QfC7wj4gebR9G1O2NjJBYX4dDb3DThXYKVRztuAqPvbfEYlk8q/8NP20Ldf2bIvGXjCyurhtG1e68N67qGh2ok0+O5tpWi+1/M48u3mwjBiSqtIFzjazfF+gfs/LrXw/bTZfi7dXT65cyWmuJa3Gu6KmsyCQ7ITAbO7tyYfL2oV+UeXk7iOO80PwT44+E/wg1L4e+D/ABcukXGoQ3UWkWsvjm2jtraCbPm77O402N5yQ07sUkiBZzgIowJftY7xf3N/ob/V8NUjpKPTqo6L1bd38+57D8K/+Cm/hO9+MfjHTfE97qVjpd3qFtH4Thh0qfULidTH5bweXaJI7SPIiyKuCSZ2AyE4+rJ2Vk3LlQwzggqRn2PP51+Z3wc/Z48Yfs6/Fux8S+EdZnsUXSriy1OWTxV4ZuLlN3lkG2M0axpEWjwyupcL/wAtSCyn2OL9p7x+mnLI3jya4hJDJKmo+CLlT68pdxg/hU06lRL34t+if6lYrL6E53w9SKVusl+if5s+lP2iNCbV/hFqFxEokm0pk1BRjOxEOJT+ELynjuB9K+b5pFjEe2RJdyhzgEGM85U56nocjI5HPUVW+IH7XfjBtG1W60/xTqUsdw0sMOkQeHfD2rSeUyEL88OrruySF/vFjwvOKNMSS1toVuGWW4WIJIy8KXwASPxya9rLarlGSaat3PBx+F9k17yd+zv+iNGwhW7Dbg67hhCB3z+oxnuOSPpRVixjaW3VF4kUkhy2FVQMkZx7569/eivS5jgsdD4V8Lan4+1Z7fSd3yyYnu2A8q34B6g8vz90YxxkrkGvZ/h/8E9E8ByNcLbrd38ww00o3YH91QeAAe3qM9ck+JeFPFXiHwJoyQaNd3umWjLJMiiFJo5AZHZnAmVwAHLDCbVz1Get3xB8WvFmoiRk8QamLGYnyYs20cyD/aeCONwR6/KDjpjiuOvRrTdk0kawlBan0Zql/a6VZNd311BYWkQJe4uHEcSAcncxIAryXXv22vhnpt1cW9n4qs9fuoRlotFVtQX6ebGDAp6/ekHQ18q/GY6h4n+HHiC9e6u77VPFDx6fayXc7zNHauwi4ZiWCmEzTN3+cjsBXCmzs/hT4Au5bdN8Gk2sl0+771y6IWJP+0xAGPcAdqyjgUviZt7S+x9Kyf8ABSe38Ty6hH4Z8H3zR2V29ibrWLyOHdKhw5WKHzd6g8cyJk59K8e8W/tp/FH4leGfEeqQeIo/Dujx29wNMh0GyWGW6EcbYmMrmSf5nB2CORNwAP8AFivP/D3wu8UX3w2sfDfhvSLjVNTktWju5w/k28BCGS5d5cHaW+ZFwCd8seOSAfqrwb+xsvgfWfCUN1rdneajuTVnhsLQpZ2Ftb7WiVWkbMhabygCVUbVkG3owivKjQhKdtlf+vU3w9GVWpGC6u3+Z5n8GP2YfEX7QOoeH/Ek3nx26TR/aPEWplrmaQzRmIhZHJkmYvIo4baDgFlr7a+Ev7P3gj4W6Sv2fSLO6uLdnFxqGoQpPcPtY5bLDCDgHagAA9TkmHw7HexeBdM0mS+iuJPIa0sXe2EXl3FrzFkp8uB5W/G3oh6918S6mfE/gHXY4PNt212wHlc4eBriIQBeOjq4OfQ1lLFJx5um5EqMufke97HnH7Pvj6/0f4Sya9fRs0dt4sXxFFFklja3ytazMqjnd5kl1KoHDBk6biB9N/EXwnpet+DrG8tdSje9hkS70+6VxJ5EwGVkQjnBBKsAcOjMpyGIrzTxx8NF8NeDbZtMtbRY7C38iWKWTy4liXY8YHH8EkUQAGOGbvXMaV4p1LwhcWtjJc6U2nXzBdNkZXVQSu77OXyQCQGZOORuUY2KG4cLmDnNRqaOV7et9vua+47cVgYcjqUPs7+lt/vT+TR6/oHiaTWdPhuVZ4nbIkj8zd5MiMUdM9yrqy5HXbWP4f1C40f4k+INL8uG30vUIYdY09Ik2LubdFdxYzztdYZM8Y+1Adq5PwZ4wvLL4p6lok1nMv8AatnFqsTQyedGGUrBOuMK4A227Z24zIxJGcV2OoD/AIqLR7lTtmWWa0cEZHlPE0jD674Ij9Aa9PVHlGZ8VvgnoHxz8GzaB4m02x1JlBW0vZoEa6sJcgx3EUuN6SIwVtykZKnsSK+KtLurq8so2uPLN1AzW0xRFCmWFjE/A4B3I25eobcDyDX6DLhQrMPlZ1XI7FiAP1Ir5U+JvgFfDvxH8WaWltAy/wBtXGrQksyn/TNs7qecffLNwONw5GTW1CbTsO7cbPoeWq8sDn5nVhyAOMZ9vp/Siuk1rwzMu0+Wq7UCgKgXj3x169Tk+9FdXMjHUovrN1cafDBJcSy29qzmCCSQskG7G4qp4UsQMleTt5qnq+qySadct8/mKjvuH0PP1q5b2vl3MZm8yKJ2wWHYGtHxXptimnpJbNbtI2S67929eM5Azzz3xnmtWQZXhn4IX3xz8SWPh7SbyxsGsYn1Cea6LsvkxgQ4UKpJbdPHwSBw3Paur+MP7E/g/wCHXw4ittUudS8Tavq0pKhlW3tIY7dGuZJGiBJKDylDAu2Q33epr0f9jDQ7bQ7c3DSSNfa1b3LQqeQtrbS28e4n1Msrr058o8kg11XjSFfGP7TNho8/m/YdN8KXbhk5xPey+TtP+15NvKw9s+tcU6j5/JHRFWR47+3p8ZNb+BvhfUIvhv4Rg8R+Ko5LXQ/DmgW8YgtxNLKtzKSFwqxMsUJblQBbSZaMHePz9/aL/wCCpXxV/Z6+MPhPw3BDBca9Y+H7HTdcsLSxtL22tb2Oea1ktxPIGwEkt5V+WQFjkknGR+qGo22laf4p8Laz4mm/svy1u572V0LCE3Dr8rYBwFknVN3RVZiflzj5x/ao/wCCPtj+1z4i16+0vw54T8Er4X1C/wBZk13w/przXPiqO/ma4W4uMz5urpkfKTArHFJHIuDEyJFOCw+GxFd0sQ0o2V/zX4srEY2rg6UasE93ay+T/BfI7L9kL9pa6+PPwVt/EEtpJaX9lqscyxGOSMySeUEMZ8wfKXhfjDOCI5H3MDmvbP7WsYtetfJuF+yXU8N6GdNqpHJKssgH+8YzKCe6z9NorhP+Cfn7Ldh8Ev2bNX0Ftc1zxBZ+I9al1QNqMCw3Glv9ltbZ7aORXYTCKW2kAn+USEsdm3lu31H4TX1v8QNJLKl1ot5E0eoFcpslVg6YAOUBZp2UgnYzlMjKE/O4mVOjVnQi7xV0n/X3fI9SnV+sxjiLWbs7ev8AV/mU/wBtLxp46j8Kw6L8OtMsH1KZD/aGoakN1nZpJujCspyHbknZtkxkMYyADX4y/wDBSL9qz48fsmfGTT/Att8Tjqmr3WlR6nqGn2mnR3NpYQs2yFSJYf8AWMYmkyqL5f7tgSWBX94/DOiT2VkunapL/aFrbsBBcnCyPGPuiQdN69Ny8MBnCnIr5c/bd/4J03X7aXijxx4eh0fw3pdpDc6f4ij1+x0SGPVHtVsBCkd5ciRJ76AXVrMPswZCEKEPmKIHuyHC4fE1eWu0l3fTscuaZhUwtD92n8tfU+Y/+Ce//BRLVvi54r8Ft4qabR/F+ntDbXVvNIfIubab908sW4n92BJvKgkpJGFPG0t96fH3xbfeGdJ8K6lYm4kurHxFHdSRo20zxC1uhJGfZw2w56FweoBH55fCv/gmO/grQfinY654gjvL3RdMRPDMbrEl7p91b5nnnCK7E7Fe1QqrOkYu4kLkspr9EfibIPFfhvRr1bdo1k0ptXlT72xZPLYn2wqucd69jExhGu6UJcyj1/E58PJVacK1mlK+57Zof2bxT4Sja3kV7bVIBJBcKPnMciZVhn2YEV4b8cdKmvPifHetGrSanptvfPjPVl8iVR7o8ERPoJDmvSP2W9W8/wALzaLcMrSaDcmNDGSxeGRPNjbnHRzLH7eT36nD8Yaol3d3EckMc0mk6xf2dyjgeZJbyTNIio/VVdHmT2KZx8oJ546MnltdHlur6NbXcNusEMsbCILMXfcHfJyRxwOnFFdXfaVFZ3DLHIs0anCyKv8ArF7NjsSOSp5ByOMYBW3MYnj2iXlurtFcXV5p9vPBJDLJB87OpB+TaMHaeAQSc0f8INbxhGt7mO93KplkVSIycBioLAMCOh46g9RgmgtnJJpy3W3dbNKIidy7g2CcY6jjv06VpaT4lOnwNGq7lzwSM7RXU79CEj0D4JeIbHw18VYorpbiGU6DY6fYpER9nhE/kX06ncd3yvLNg8n5TnoK7G1muZPiJ8WLy1tWutS8O3GmSW9vHhpLuBLFJXjTPSSTfcxLngMVbvXi/gtbrxb4os47aG5m1CxmhjVI1Z3uI4owwCgDJ3RL5Z255YivrD4e6MND8eavrX2ETPrKQGdpW2SJthjibjHXMO7nGCMZ644po6NVqcL4l1W1tPHPgm8h2XFlrj3FpbXqMcIZIRNER2w5hC8jOSuMc10E3gu2v/D0OjyW+3SoNqrZwu0EAVeibUIBj7FD8pHBBFP+KXwonsLZrTTYUk0mS7GtaW0X/MPmBPmbe4VTIX2fiOQwHa6fDHrvh+21CGPatym5k7xP0dD7qwIP0rxMwotTVWD3PTwuIXsvZSVzBSFbCyhhiRIYIFCRxIoVIlAACqBwAAAAB0AFVbHWYb+/ureNlka1YJKVYNsbAO046NhlODzgg9607+LyzgZ68ZqBIdu5lX7xySBjJxjmvFa1OiMkOHSsfxXoEfijTFtrhrxUXO1ra7mtZkBxuCyRMrqGwMgMA2BkGtqKEuea0bDS1kDOVYqoycDNXT5k/ddmLmj9pXPK5vhNY6doy6XpOlafZf2nKIvLhhWJZcbpGLlcE5AclmySzc5LHPQXfwxbSbGSxkIbydDFnJJ1LstsqqPwUH6ls12Pg3Q7rxB8RTcuGt7PTrUqsPBIaQjG8jIzhWJUEgDyjyRmk8XazGurXkm7y4lJ3Pj+HaBnHsiAkehr6HAUuSnfq9TixmIc6ijskrHOfs+6TDpXjTXo2UrcCwsI7gE/cYSXjD6fK4ri/F2jyXet6TrUbsIdbfU7uQfwjZOdyntkAqwPsw6Zq1r3jhUk1a102Vr7xN4wwPsVofNuYLSIMFBVckM7NKN2AFRgSVO3Olqlo/gD4eXUniKa3h1K8sbjT9J04OrTQpO8jSSsASN3zkkjgKoUncwUd3W5zSerbOP8TNa21/I1i1wYWUcSsFLkDvgHGDnBHbr2wVyOq+I/kPzfr0orQws2eS6dcq3yrnLcPnoRkED8x/Kuk061WJMJ/wAtSBx3H+H+FcXAs67ZAuxclQxzhiMZ/LI/MVpWHiX7GwV9zMpz8vrXXIzXke5fCrSktpmvFm8l7FNz7HKM7AhgoKnJBVJeOn8x79pOow6P4f8AtTK915Z8twsn7x9z7SQ2Qc5568nPQnNfIvwp+IcmufEBtFjkaPzILGD/AIHdXEttGeP7u+Q/RhXpmrfH2x017bSnuIVuI7iS6uLeSTasiLM8aQuwOYxJJ8pkAIjVGZsAZriq9zo15T3L/ha2mr4l0GxtdJk023jn8yUyfLuDxsMhAcHIfO4knHr1rlPix4u1n4K/Eq3XR7OHVNF1N1iu9OaTynDSSRxQyQyMPLRvMkWM+Yyo2Uyy43ri6v8AEez8SfDzWNSjuY4rWxm2OJCsnkyx5dlkCnCAuzLCy8BVQDKSFG80/wCCh/x303wh4e+G+pateR2el+OLS50aa7limuLeGW4hge3Z4ImQzZkJVEd0jEjxs7Kqk1xykpwlE0pxcZJ9D1n4VfHvwf8AtEaDPq3g7W7TV4LKY299AMx3elzAkGG5gbEkMgII2uBnGQWGCb994HtdU8TWmrtc6pb3VntAEGoSxQyKpJ2vGG2MpLcgjnjOQBX4yt8FvFXgD492/wARrXxxrXwOkbUQ2t31pLafadOHnPaXxj0+JfJ+xxanGgniknl2QahaStEyEtX178H/APgpX8TNV0nWLrWI/h/q3wzs3NnonxYukl0WPxLKmFkFtpDFpL+YSCSL/RWSJnjJXAIUeFUw/v2jr1/roexGLSUou19P+AfoXcQWul6Y19d3VvaWcXMks0gjRR7seK5jSfjjpPjLS7htEs9WutLhBzrBtDHZSEdkZ9vmHIxgDHQgt0r468DeL9Y1O9s/F3ibUPEureG5ZY4rzxP45hjsLOzWWWPyL+z0aJv9GgjYIGe5bLRzFmQha+vfhZ8RtFaORdsf2yCKW583UGCR2BjkMd5Ei4CosVxknYFXZNGd2CK7KNOko8+5x1JSTtH7zvfAN83h34f6tqd1b3FrJAHncXA2u+2MOCfqTx0+gHFfJ/7UPx31zwTcTaXfRy2cO8RPDDj7QWJzG5wS3luApD9OeSM8+weK/jxp+ufBPxVLpd9NqiRXqW0ctvEGM6GFZEMQcBZAwjKqTlHPOSpzXxT+0P8AFuH4c6p4ij1KSC40vThNHdO9/JNa65pJlWO6064vI3jk1C8smkikFtbPHbRohDyYzXpSl7qb0uckY+8+p0X7P/j+38ea14lim+yxx2dgISiXCySRGVm++BnaR5IIHJHX0r1A6qsfg2S8j2wzOx3GJdu/JZWBx1GM/gK/Pf8AY3+LDH46eINDXVpGuv7EvfMgfZCr+XPB5LRRKAoPlO7HAzjceRzX3D4Nu77XfgHNeLD5kipJKwx90C4ZfywQK6cPbkHXTjJ38ihquusPl+YcZ59xn+WKK41tdmcOGRXaUDBJbMfOTgevbnPX8aK1Oc0LiyWxgUqFbcc5PX8qa1wRYrbNHb/LOZ/N8j/SORgqX/ujGdvqSas3c9vLo800syR3MbLtg2EtMCDlg3QYIHBI+9x3qlrEllaX0f2O4e7ikiRy5iMflOfvJjJzg9+9dLMkdl+zto73nxj0OZo2/wCJlr0EJcngpZW5vWHHT5gB9WFfKt1+0dd6N/wUZ+IHgrUNSaz1nUvG1zo2l3kBMU+jWjuZvttixYL9o+zmKLLEgAuCCuQ/17+y9eWNl8UfCdxeXCho9U1KMKWxHbi8sIFhkdj/AHm025jA7tIO/B/Gf9sP4lap4r/ak8YavqUVvBqEd+LqAyD7OAypsXdOzptYwNbPiEO6mRTwQVrzcVdrQ9HC07/cfq/8UPGd98MfDdppFjM0cK7bHTprVd0dzDBFNKYFjd1ZsOgMlhIwlhZnktGkBktBn/t8yR+N/Dv7IvheRry4h1jVLia5SzmjiumtrOyjeQRs5A5QBSSQMN34FfMX7M37eGtftJ/BvxJH4ohtb6a0tF0N7m4aCG8vZrkERpchx9muShhGDmC5dWJihmdHJ1f+CnGv32ueNfgqtvbrLH8N/g/qnjOWMXb2k9lcX4NnbSLJHPBPGwna3YmKRmxwYZlbaOPC8/JL2mjute5VaMYuPJ5u39fI8R8V/sM+Pm8K/DTWNFuPH/xW8I+J/DFj4k1Xw9qk8lm8l3Hp9u9xavctCBKrpDarB98lYfL6RxtXcf8AD5/xZ+z5H/wjrfBLS/D+rXB+1XEGui8lv5o5CxZ5DNBHKzu3JkdmJOc/N0+a/wBsP9tjVPEVpo/gfwn4y8SWXhHw2Le2isLvWbuQf6MhSG7WWS3trkKwCFLdw6qApJ3DA+fNU12Ky169S+t7+4uLaMX1+93bSRtAGIxM27GN29cEksxYYzW+DouNNe0sdEsUlC0N+t7P9L/ifZvg3/gsr4k1L4sG41TQfBsng27Q6ZqOiXy3Vxp2kxy5R7qMNI8kWxXJkjj2h4wVAU7SPob4lfGXXvg14ttofHPiS7ivLNbfUdKvvGOnCOTVIPLFvaanb+HFP+rlS2htbyXUpWZD9mutgBr8qr3VrGef7ZHIzw8IlyWHmoD0VyOGU54Jz1Hfk7/hH4jrBDHYTMlnqEblrK8aMzNOQu0W79SY3QeWBhhtKqBlVJKuHjD34L1/zOfnc3aTP2M8Dftb2fxw+HvjZbGS4nuNQ3f2nY6rqb6jexXKWM4WO7lCRwliIH+W0H2dY3RY2OCa+Q/2v/2nfEXxm8U3+pX8lmsfhe5kgiEG210fwvBuZPKijGS2QQHChpNpDEA7a5H/AIJcftE2N3+0cvhGSB7fTddTZD9ok3XDSQWtwUt5xk4kjSa4j+b5yqqGwQBXE/FzU/CPwc8Ta94duNUtbbxL4fvrhbV8SXl9aXHmySjaFz5eXkJI3KCHJI+bmK0bwhK12ro0w9ueUbpbO70O68F6RrVhHp97ptrPo10Yvt1pPHixs4wyMBMgBM90GUnDykK4PzfxLX67/sbXcHjz9jDUtXhjjX7fYymFUO5QPsyXGFJycGSQ4J6hQfevwE8dftg6pJfSXHh2E2O5HWI30glFqrLEzrDFnYoWWNnTdvwZXAGTiv1Y/wCDen/govoPx3+Dz/A/xhexWPxD0dXbThLiNfE2mrbxRZiOfmuYY4v3ifeZAJRuAl8vShTqRvJ7E47EUJKMIatddl6HawtGuqTKfvxArgc5YcGiqM9rcWupbZd32pQpl4437QW/8eJorsPPLupTt57/AO8efxpkB8+QH7u4ngdvaiiuqRlHYXXLdpI/H1ss00Mdt4Ig1KHy22mG6glZ4Zl/20eeRh2y3IPSvwpv/G+sxfES78SrqU39ueJ52bULt445ZJZJiZZJRvU7XZ1B4wPbpgorjrap3O1Nr2dj6o/4Jm+CYbP9vL4YaPDfavHY+OPEdlbeIEW+kH9swpHeTeTcc/vIzJDE2xsqDGpUKQCK/wDwU++OPiS+/bi+LlgdQkjs4NJ8H6RLBGzLFeWVvYQXqW0qZ2tGbuKK4PAbzI1wVXKkorjj8H9eRdbSRzn7Svxd1TwZ8GfBPhvSI7XTI9O8PR+Kv7Rtg8epXFxcXtxG8Tzht3kKEQqibTlFyxxivmrWfjh4g1vU0+3XTXzSN8zXUslwxIyM5dyc8n86KK6cGlyM9HM2701/dRa1t99xZvtjC38bLPEFAjfG3nHvuOfwrH1i5ltLS6khllhkhiYxujlWTAOMEc0UVueTLYh/Z28Yah8Nfj94D1jSpvJu9O1+xuIQR8gImjypAx8rKSpHdSRxX3x+21+zf4d+Kf8AwU18X2t81/ax6h4asNXm+ySrGTcLD9nDcqeqW6E+rFietFFaUkrWPPnJ/wBfI+Gbm2W3uJI/mfy5zEGc5YjPf8vpXuP7Id/J4L/a7+EuqaWxstQh8X6VbxzxEq8QluY4mZT2YK7YI7nv0ooohu0aVPs/I/Y/VdcuLi71Hcy/6ZfXnnAIuGK3k5BHHy/RcDHGMYFFFFYm8tz/2Q==
// ==/UserScript==
var Solve = /** @class */ (function () {
    function Solve() {
    }
    Solve.sendForSolve = function (node) {
        var image = document.getElementsByClassName('fbc-imageselect-payload')[0];
        if (image != undefined && !this.init) {
            var challenge = document.getElementsByTagName('STRONG')[0].textContent;
            if (challenge == 'cars') {
                document.getElementsByClassName('fbc-button-reload fbc-button')[0].click();
                return;
            }
            this.init = true;
            console.log('http://localhost:5000?tag=' + encodeURIComponent(image.src) + "&challenge=" + encodeURIComponent(challenge));
            GM_xmlhttpRequest({ method: 'GET', url: 'http://localhost:5000?tag=' + encodeURIComponent(image.src) + "&challenge=" + encodeURIComponent(challenge),
                responseType: 'text', onload: function (response) {
                    console.log(response.response);
                    var number_arr = response.response.replace(/[\r\n↵]/g, " ").split(' ').splice(1);
                    console.log(number_arr);
                    var found_three = 0;
                    number_arr.forEach(function (number, index) {
                        if (number > 1000) {
                            document.getElementById('checkbox-' + index).click();
                            found_three++;
                        }
                    });
                    if (found_three > 2)
                        document.getElementsByClassName('fbc-button-verify')[0].firstChild.click();
                    else
                        document.getElementsByClassName('fbc-button-reload fbc-button')[0].click();
                } });
        }
    };
    Solve.init = false;
    return Solve;
}());
var main = /** @class */ (function () {
    function main() {
        var _this = this;
        this.captcha_open = 0;
        //js
        if (window.location.pathname.indexOf('bframe') > -1) { }
        //no js
        else if (window.location.pathname.indexOf('fallback') > -1) {
            var body_observer = new MutationObserver(function (mutations_list) {
                mutations_list.forEach(function (mutations) {
                    [].forEach.call(mutations.addedNodes, function (node, index) {
                        Solve.sendForSolve(node);
                    });
                });
            });
            body_observer.observe(document.body, { childList: true, attributes: true, subtree: true });
            //force trigger
            document.body.appendChild(document.createTextNode(""));
        }
        //4chanX page
        else if (window.location.pathname.indexOf('4chan')) {
            document.addEventListener('QRDialogCreation', function (e) {
                var qr_observer = new MutationObserver(function (mutations_list) {
                    mutations_list.forEach(function (mutation) {
                        var open_condition = (mutation.type == "attributes"
                            && mutation.target.className.indexOf('focus') > -1
                            && mutation.target.className.indexOf('noscript-captcha') > -1
                            && mutation.target.className.indexOf('captcha-open') == -1);
                        if (open_condition && _this.captcha_open == 1) {
                            console.log('mclick');
                            _this.captcha_open = 2;
                        }
                        else if (open_condition && _this.captcha_open == 2) {
                            var captcha_counter = document.getElementsByClassName('captcha-counter')[0].firstChild;
                            console.log('uclick');
                            captcha_counter.click();
                            _this.captcha_open = 1;
                        }
                        else if (open_condition && _this.captcha_open == 0) {
                            var captcha_counter = document.getElementsByClassName('captcha-counter')[0].firstChild;
                            if (parseInt(captcha_counter.textContent.split(" ")[1]) < 2) {
                                if (!_this.captcha_open) {
                                    console.log('dclick');
                                    captcha_counter.click();
                                    _this.captcha_open = 1;
                                }
                            }
                        }
                    });
                });
                qr_observer.observe(document.getElementById('qr'), { attributes: true });
                //force trigger
                document.body.appendChild(document.createTextNode(""));
            }, false);
        }
    }
    return main;
}());
if (window.localStorage.getItem('captcha-log') == '0') {
    new main();
    window.localStorage.setItem('captcha-solve', '1');
}
else {
    alert('Captcha Solver running with aquisition(might not be, try one more time)');
}
window.localStorage.setItem('captcha-log', '0');

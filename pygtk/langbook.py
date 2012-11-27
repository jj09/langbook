#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import random

class Base:
  def destroy(self, widget, data=None):
    #print 'You clicked the Close Button'
    gtk.main_quit()


  def about_win(self, widget):
    about = gtk.AboutDialog()
    about.set_program_name('Langbook')
    about.set_version('0.1')
    about.set_copyright('(c) Jakub Jedryszek')
    about.set_comments('This is interactive dictionary for foreign languages learning')
    about.set_website('http://www.langbook.com')
    #about.set_logo(gtk.gdk.pixbuf_new_from_file('pics/tux-icon.png'))
    about.run()
    about.destroy()


  def load_dict(self):
    with open('dict.csv', 'rU') as f:
      langs = f.readline().split(',')
      langs = list(i.rstrip('\n')[1:-1] for i in langs)	# remove " from begin and end
      self.dict = []
      for line in f:
        phrases = line.split(',')
        phrases = list(i.rstrip('\n')[1:-1] for i in phrases)	# remove " from begin and end
      
        phrase = {}
        for i in range(len(langs)):		# do it more clean!
          phrase[langs[i]] = phrases[i]
        self.dict.append(phrase)

 
  def map_langs(self):
    self.lang_map = {}
    for lang in open('lang_map.csv', 'rU').readlines():
      mapping = lang.split(',')
      mapping = list(i.rstrip('\n')[1:-1] for i in mapping)	# remove " from begin and end
      self.lang_map[mapping[0]] = mapping[1]


  def set_lang_combos(self):
    for k in self.lang_map.keys():
      self.combo_your.append_text(k)
      self.combo_learn.append_text(k)
    # to do add default values loading (from file?)
    self.combo_your.set_active(0)
    self.combo_learn.set_active(1)


  def start_quiz(self, widget):
    self.score = 0
    self.your_lang = self.lang_map[self.combo_your.get_active_text()]
    self.learn_lang = self.lang_map[self.combo_learn.get_active_text()]
    self.window.remove(self.box_main)
    self.window.add(self.box_quiz)
    self.window.show_all()
    self.load_question()


  def load_question(self):
    question_no = random.randint(0, len(self.dict)-1)
    self.label_question.set_text(self.dict[question_no][self.your_lang])
    self.answer = self.dict[question_no][self.learn_lang]
    answers = []
    answers.append(self.answer)
    for i in range(3):
      while self.dict[question_no][self.learn_lang] in answers:
        question_no = random.randint(0, len(self.dict)-1)
      answers.append(self.dict[question_no][self.learn_lang])      
    random.shuffle(answers)
    
    for i in range(len(self.button_answers)):
      self.button_answers[i].set_label(answers[i])

    self.button_answers[0].set_active(True)
    self.button_check_answer.set_sensitive(True)


  def check_answer(self, widget):
    active = [r for r in self.button_answers[0].get_group() if r.get_active()][0]
    if self.answer == active.get_label():
      self.score += 1
    else:
      self.score -= 1

    # display icons for good (and wrong if necessary) answers
    for i in range(len(self.button_answers)):
      if self.button_answers[i].get_label() == self.answer:
        self.box_answers[i].pack_start(self.image_good)
        self.image_good.show()
      elif self.button_answers[i].get_label() == active.get_label():
        self.box_answers[i].pack_start(self.image_wrong)
        self.image_wrong.show()
      
    self.update_score()
    self.button_check_answer.set_sensitive(False)


  def next_question(self, widget):
    self.load_question()
    self.remove_answer_icons()


  def remove_answer_icons(self):
    for i in range(len(self.button_answers)):
      if len(self.box_answers[i].get_children())>1:
        self.box_answers[i].remove(self.box_answers[i].get_children()[1])


  def cancel_quiz(self, widget):
    self.window.remove(self.box_quiz)
    self.window.add(self.box_main)
    self.window.show_all()
    info_dialog = gtk.Dialog('Your result', None, 0,
                   (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
    info_dialog.set_size_request(200, 100)
    label_result = gtk.Label('Your result: %s' % self.score)
    info_dialog.vbox.pack_start(label_result)
    label_result.show()
    response = info_dialog.run()
    info_dialog.destroy()
    self.score = 0
    self.update_score()
    self.remove_answer_icons()


  def update_score(self):
    self.label_score.set_label('Score: %s' % self.score)    


  def init_main_page(self):
    self.box_main = gtk.VBox()
    self.window.add(self.box_main)

    self.box_combos = gtk.VBox()
    self.box_main.pack_start(self.box_combos, False, False, 0)

    self.box_combo_your = gtk.HBox()
    self.box_combos.pack_start(self.box_combo_your)
    self.label_your = gtk.Label("Your language: ")
    self.box_combo_your.pack_start(self.label_your)
    self.combo_your = gtk.combo_box_entry_new_text()
    self.box_combo_your.pack_start(self.combo_your)

    self.box_combo_learn = gtk.HBox()
    self.box_combos.pack_start(self.box_combo_learn)
    self.label_learn = gtk.Label("Language to learn: ")
    self.box_combo_learn.pack_start(self.label_learn)
    self.combo_learn = gtk.combo_box_entry_new_text()
    self.box_combo_learn.pack_start(self.combo_learn)

    self.box_buttons = gtk.HBox()
    self.box_main.pack_start(self.box_buttons, False, False, 10)

    self.button_start = gtk.Button('Start')
    self.box_buttons.pack_start(self.button_start, False, False, 10)
    self.button_start.connect('clicked', self.start_quiz)

    self.button_about = gtk.Button('About')
    self.box_buttons.pack_start(self.button_about, False, False, 10)
    self.button_about.connect('clicked', self.about_win)


  def init_quiz_page(self):
    self.box_quiz = gtk.VBox(False, 0)

    self.label_score = gtk.Label('Score: 0')
    self.box_quiz.pack_start(self.label_score, False, True, 0)

    self.separator = gtk.HSeparator()
    self.box_quiz.pack_start(self.separator, False, True, 0)

    self.fixed_label = gtk.Fixed()
    self.box_quiz.pack_start(self.fixed_label, False, False, 0)
    self.label_question = gtk.Label()
    self.fixed_label.put(self.label_question, 0, 0)

    self.box_answers = []
    self.button_answers = []

    self.box_answers.append(gtk.HBox())
    self.box_quiz.pack_start(self.box_answers[0], False, False, 0)
    self.button_answers.append(gtk.RadioButton(None))
    self.button_answers[0].set_active(True)
    self.box_answers[0].pack_start(self.button_answers[0], False, False, 0)

    self.box_answers.append(gtk.HBox())
    self.box_quiz.pack_start(self.box_answers[1], False, False, 0)
    self.button_answers.append(gtk.RadioButton(self.button_answers[0]))
    self.box_answers[1].pack_start(self.button_answers[1], False, False, 0)

    self.box_answers.append(gtk.HBox())
    self.box_quiz.pack_start(self.box_answers[2], False, False, 0)
    self.button_answers.append(gtk.RadioButton(self.button_answers[1]))
    self.box_answers[2].pack_start(self.button_answers[2], False, False, 0)

    self.box_answers.append(gtk.HBox())
    self.box_quiz.pack_start(self.box_answers[3], False, False, 0)
    self.button_answers.append(gtk.RadioButton(self.button_answers[2]))
    self.box_answers[3].pack_start(self.button_answers[3], False, False, 0)

    self.separator = gtk.HSeparator()
    self.box_quiz.pack_start(self.separator, False, True, 0)

    self.box_buttons = gtk.HButtonBox()
    self.box_buttons.set_layout(gtk.BUTTONBOX_START)
    self.box_quiz.pack_start(self.box_buttons, False, False, 0)

    self.button_check_answer = gtk.Button('Check')
    self.box_buttons.pack_start(self.button_check_answer, False, True, 0)
    self.button_check_answer.connect('clicked', self.check_answer)

    self.button_next_question = gtk.Button('Next')
    self.box_buttons.pack_start(self.button_next_question, False, True, 0)
    self.button_next_question.connect('clicked', self.next_question)

    self.box_cancel = gtk.HButtonBox()
    self.box_cancel.set_layout(gtk.BUTTONBOX_END)
    self.box_quiz.pack_start(self.box_cancel, False, False, 0)

    self.button_cancel = gtk.Button('Cancel')
    self.box_cancel.pack_start(self.button_cancel, True, False, 0)
    self.button_cancel.connect('clicked', self.cancel_quiz)


  def init_answers_icons(self):
    self.pix_good = gtk.gdk.pixbuf_new_from_file('good.png')
    self.pix_good = self.pix_good.scale_simple(20, 20, gtk.gdk.INTERP_BILINEAR)
    self.image_good = gtk.image_new_from_pixbuf(self.pix_good)

    self.pix_wrong = gtk.gdk.pixbuf_new_from_file('wrong.png')
    self.pix_wrong = self.pix_wrong.scale_simple(20, 20, gtk.gdk.INTERP_BILINEAR)
    self.image_wrong = gtk.image_new_from_pixbuf(self.pix_wrong)


  def __init__(self):
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.set_size_request(320, 200)
    self.window.set_title('Langbook 0.1')
    self.window.connect('destroy', self.destroy)

    # init pages
    self.init_main_page()
    self.init_quiz_page()
    self.init_answers_icons()    

    # load data
    self.load_dict()
    self.map_langs()
    self.set_lang_combos()

    self.window.show_all()
    self.box_quiz.hide()

 
  def main(self):
    gtk.main()


if __name__ == '__main__':
  base = Base()
  base.main()

VERSION_SRC := lib/Version.py

dist:
	git archive --prefix=themis-`cat .version`/ master | bzip2 > themis-`cat .version`.tar.bz2


gittag:
        ifneq ($(TAG),)
	  @git status -s > /tmp/git_st_$$$$;                                         \
          if [ -s /tmp/git_st_$$$$ ]; then                                           \
	    echo "All files not checked in => try again";                            \
	  else                                                                       \
	    echo '$(TAG)'                                         >  .version      ; \
	    $(RM)                                                    $(VERSION_SRC); \
	    echo 'class Version(object):'                         >> $(VERSION_SRC); \
	    echo '  def __init__(self):'                          >> $(VERSION_SRC); \
            echo '    pass'                                       >> $(VERSION_SRC); \
	    echo '  def tag(self):'                               >> $(VERSION_SRC); \
            echo '    return "$(TAG)"'                            >> $(VERSION_SRC); \
	    echo '  def git(self):'                               >> $(VERSION_SRC); \
            echo '    return "@git@"'                             >> $(VERSION_SRC); \
	    echo '  def date(self):'                              >> $(VERSION_SRC); \
            echo '    return "$(VDATE)"'                          >> $(VERSION_SRC); \
	    echo '  def name(self):'                              >> $(VERSION_SRC); \
            echo '    sA = []'                                    >> $(VERSION_SRC); \
            echo '    sA.append(self.tag())'                      >> $(VERSION_SRC); \
            echo '    sA.append(self.git())'                      >> $(VERSION_SRC); \
            echo '    sA.append(self.date())'                     >> $(VERSION_SRC); \
            echo '    return " ".join(sA)'                        >> $(VERSION_SRC); \
            git commit -m "moving to TAG_VERSION $(TAG)" .version    $(VERSION_SRC); \
            git tag -a $(TAG) -m 'Setting TAG_VERSION to $(TAG)'                   ; \
	    git push --tags                                                        ; \
          fi;                                                                        \
          rm -f /tmp/git_st_$$$$
        else
	  @echo "To git tag do: make gittag TAG=?"
        endif

tags:
	find . \( -regex '.*~$$\|.*/\.git\|.*/\.git/' -prune \)  \
               -o -type f > file_list.1
	sed -e 's|.*/.git.*||g'                                  \
            -e 's|^.*/TAGS$$||g'                                 \
            -e 's|./makefile||g'                                 \
            -e 's|./configure$$||g'                              \
            -e 's|/.DS_Store$$||g'                               \
            -e 's|.*\.tgz$$||g'                                  \
            -e 's|.*\.tar\.gz$$||g'                              \
            -e 's|.*\.tar\.bz2$$||g'                             \
            -e 's|.*\.csv$$||g'                                  \
	    -e 's|.*\.aux$$||g'                                  \
	    -e 's|.*\.pyo$$||g'                                  \
	    -e 's|.*\.pyc$$||g'                                  \
	    -e 's|.*\.fdb_latexmk$$||g'                          \
	    -e 's|.*\.fls$$||g'                                  \
	    -e 's|.*\.nav$$||g'                                  \
	    -e 's|.*\.out$$||g'                                  \
	    -e 's|.*\.pdf$$||g'                                  \
	    -e 's|.*\.snm$$||g'                                  \
	    -e 's|.*\.toc$$||g'                                  \
	    -e 's|.*\.vrb$$||g'                                  \
            -e 's|^#.*||g'                                       \
            -e 's|/#.*||g'                                       \
            -e 's|\.#.*||g'                                      \
            -e 's|.*\.pdf$$||g'                                  \
            -e 's|.*\.used$$||g'                                 \
            -e 's|./.*\.log$$||g'                                \
            -e 's|./testreports/.*||g'                           \
            -e 's|./config\.status$$||g'                         \
            -e 's|.*\~$$||g'                                     \
            -e 's|./file_list\..*||g'                            \
            -e '/^\s*$$/d'                                       \
	       < file_list.1 > file_list.2
	etags  `cat file_list.2`
	$(RM) file_list.*

world_update:
	@git status -s > /tmp/git_st_$$$$;                                         \
        if [ -s /tmp/git_st_$$$$ ]; then                                           \
            echo "All files not checked in => try again";                          \
        else                                                                       \
	    branchName=`git status | head -n 1 | sed 's/^[# ]*On branch //g'`;	   \
            git push        github     $$branchName;                               \
            git push --tags github     $$branchName;                               \
            git push        rtm_github $$branchName;                               \
            git push --tags rtm_github $$branchName;                               \
        fi;                                                                        \
        rm -f /tmp/git_st_$$$$

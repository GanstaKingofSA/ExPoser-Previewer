init python in exp_pasrer:  
    from renpy import store

    class ExPoserCharacter(object):
        def __init__(self, tag):
            self.tag = tag
            self.attributes_map = {}

    class AttributeDict(object):
        def __init__(self):
            self.attributes = {}
        
        def append(self, key, value):
            if not self.attributes.has_key(key):
                self.attributes[key] = value
            else:
                self.attributes[key] = [*set(self.attributes[key] + value)]

    characters = {}
    
init 999 python hide:
    from renpy import store
    from store.exp_pasrer import ExPoserCharacter, AttributeDict

    # Automatically get all Dynamic Characters with a Image Tag
    characters = []

    for var, c in store.__dict__.items():
        char = getattr(store, var)
        if isinstance(char, ADVCharacter):
            if char.__dict__['dynamic'] and char.__dict__['image_tag']:
                characters.append(char.__dict__['image_tag'])

    # For Every Character from the characters array
    for c in characters:
        # For the character name and image defined in Ren'Py
        for name, image in renpy.display.image.images.items():
            # Set name and attribute as tag and tag_rest
            tag, tag_rest = name[0], name[1:]
            if tag != c: continue
            # Only check for LayeredImages
            if not isinstance(image, LayeredImage): continue

            exp_pasrer.characters.setdefault(c, ExPoserCharacter(tag))

            last_group = None

            # Stores the group and attributes in a dict class
            attr_dict = AttributeDict()

            # For every attribute
            for attr in image.attributes:
                # do not include the always attribute
                if isinstance(attr, layeredimage.Always): continue

                if last_group is None or attr.group != last_group:
                    last_group = attr.group

                # Add "" first to remove certain areas
                attr_dict.append(attr.group, ["", attr.attribute])

            exp_pasrer.characters[c].attributes_map[tag_rest] = attr_dict

    # import pprint

    # Translate all groups and attributes for every character's pose to ExPoser Previewer
    for tag, c in exp_pasrer.characters.items():
        for pose, attr_dict in c.attributes_map.items():
            fileName = "%s_%s" % (tag, "".join(pose))

            with open(os.path.join(config.gamedir, "exposer_defs", fileName + "_def.rpy"), "w") as edf:
                edf.write("init python:\n")
                edf.write(
                    "    ExposerPreviewerDefinition(\n"
                )
                edf.write("        char=\"%s (%s)\",\n" % (tag.capitalize(), " ".join(pose).capitalize()))
                edf.write("        pose=\"%s %s\",\n" % (tag, " ".join(pose)))
                for g, attributes in c.attributes_map[pose].attributes.items():
                    edf.write("        {0}={1},\n".format(g, sorted(attributes)))
                edf.write("    )\n")

            # print("%s %s" % (tag, " ".join(pose)))
            # pprint.pprint(attributes)
            # print("\n")